from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.db.models import Sum
from .models import Balance, Miner, HashRate, TimeStart
from .forms import CalculateForm
import datetime


def time_to_minutes(time_):
    return time_.seconds // 60 + time_.days * 24 * 60


class StatisticView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'statistic/main.html',)


class GetStatisticJson(View):
    def get(self, request, *args, **kwargs):
        balance = Balance.objects.get(description='current').value / 1_000_000_000
        all_time = self.get_working_time()
        stats = {
            "balance": balance,
            "time": time_to_minutes(all_time),
            "hr": self.get_sum_hr() / (time_to_minutes(all_time) // 5) / 1_000_000,
            "miners": [self.get_miner_info(miner) for miner in Miner.objects.filter(visible=True)],

        }
        return JsonResponse(stats)

    def get_miner_info(self, miner):
        all_time = self.get_working_time()
        sum_hr = self.get_sum_hr()
        miner_sum_hr = self.get_sum_miner_hr(miner)
        hr_avg_all, hr_avg = self.get_hashrate_avg(miner, all_time)
        return {
            "name": miner.name,
            "worker_name": miner.worker,
            "is_online": miner.is_online,
            "working_time": self.get_working_time_for_miner(miner),
            "general_hr": hr_avg_all / 1_000_000,
            "hr": hr_avg / 1_000_000,
            "share": miner_sum_hr / sum_hr,
        }

    @staticmethod
    def get_sum_miner_hr(miner):
        begin_time = TimeStart.objects.get(name='begin').time
        hrs = HashRate.objects.filter(miner=miner, time__gte=begin_time)
        if not hrs:
            return 0
        return hrs.aggregate(hr_sum=Sum('hr'))["hr_sum"]

    @staticmethod
    def get_sum_hr():
        begin_time = TimeStart.objects.get(name='begin').time
        return HashRate.objects.filter(time__gte=begin_time).aggregate(hr_sum=Sum('hr'))["hr_sum"]

    @staticmethod
    def get_working_time():
        now_time = datetime.datetime.now(datetime.timezone.utc)
        begin_time = TimeStart.objects.get(name='begin').time
        return now_time - begin_time

    @staticmethod
    def get_working_time_for_miner(miner):
        begin_time = TimeStart.objects.get(name='begin').time
        miner_hashrates = HashRate.objects.filter(miner=miner, time__gte=begin_time, hr__gt=0)
        count = miner_hashrates.count()
        if not count:
            return 0
        return (count - 1) * 5

    @staticmethod
    def get_hashrate_avg(miner, all_time):
        begin_time = TimeStart.objects.get(name='begin').time
        all_count = time_to_minutes(all_time) // 5
        miner_hashrates = HashRate.objects.filter(miner=miner, time__gte=begin_time)
        if not miner_hashrates:
            return 0, 0
        count = miner_hashrates.count()
        sum_hr = miner_hashrates.aggregate(hr_sum=Sum('hr'))["hr_sum"]
        avg_hr_in_all_time = sum_hr // all_count
        if count == 1:
            return avg_hr_in_all_time, sum_hr
        avg_hr_in_working = sum_hr // (count - 1)

        return avg_hr_in_all_time, avg_hr_in_working


class GetCalculator(View):
    def get(self, request, *args, **kwargs):
        form = CalculateForm()
        return render(request, 'statistic/stat_result.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = CalculateForm(request.POST)
        stats = {}
        if form.is_valid():
            time = form.cleaned_data['end_time'] - form.cleaned_data['begin_time']
            print(form.cleaned_data['end_time'] - form.cleaned_data['begin_time'])
            print(form.cleaned_data['miners'])
            print(request.POST)
            stats = {
                "time": time,
                "miners": [self.get_miners_info(miner=miner, form=form) for miner in Miner.objects.all()],
            }
            print(stats)

        return render(request,
                      'statistic/stat_result.html',
                      {
                          'form': form,
                          'stats': stats,
                      })

    def get_miners_info(self, miner, form):
        begin_time = form.cleaned_data['begin_time']
        end_time = form.cleaned_data['end_time']
        sum_hr = HashRate.objects.filter(time__gte=begin_time, time__lte=end_time).aggregate(hr_sum=Sum('hr'))["hr_sum"]
        miner_sum_hr = self.get_sum_miner_hr(miner, begin_time, end_time)
        res_share = self.get_result_share(miner, form.cleaned_data['miners'], begin_time, end_time)
        return {
            "miner": miner,
            "share": miner_sum_hr / sum_hr,
            "res_share": res_share,
            "payment": res_share * form.cleaned_data["balance"]
        }

    @staticmethod
    def get_sum_miner_hr(miner, begin_time, end_time):
        hrs = HashRate.objects.filter(miner=miner, time__gte=begin_time, time__lte=end_time)
        if not hrs:
            return 0
        return hrs.aggregate(hr_sum=Sum('hr'))["hr_sum"]

    def get_result_share(self, miner, miners, begin_time, end_time):
        hr_miner = self.get_sum_miner_hr(miner, begin_time, end_time)
        all_sum_hr = HashRate.objects.filter(
            time__gte=begin_time,
            time__lte=end_time,
            miner__in=miners
        ).aggregate(hr_sum=Sum('hr'))["hr_sum"]

        if miner in miners:
            return hr_miner / all_sum_hr
        return 0
