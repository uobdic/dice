import os
from time import localtime, strftime

import classad
import tabulate

startd_history_file = (
    "~/pCloudDrive/DICE/incidents/2023.07.05/hd75/startd_history.other"
)
startd_history_file = os.path.expanduser(startd_history_file)


def get_ads_from_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    ads = []
    stop_at = "*** Offset"
    current_ad = []
    for line in lines:
        if line.startswith(stop_at):
            ads.append("\n".join(current_ad))
            current_ad = []
            continue
        current_ad.append(line)
    return [classad.parseOne(ad) for ad in ads]


def noop(x):
    return x


def get_ad_info(ads, time_fmt_func=noop):
    start_end_ids = []
    header = ["JobStartDate", "CompletionDate", "ClusterId", "Owner"]
    for ad in ads:
        start_end_ids.append(
            [
                time_fmt_func(ad["JobStartDate"]),
                time_fmt_func(ad["CompletionDate"]),
                ad["ClusterId"],
                ad["Owner"],
            ]
        )
    return header, start_end_ids


ads = get_ads_from_file(startd_history_file)

cms_ads = [ad for ad in ads if ad["Owner"].startswith("cms")]
cms_pilot_ads = [cad for cad in cms_ads if "pil" in cad["Owner"]]

ten_minutes_in_epoch = 600
event_time = 1688526720


def filter_ads_for_event(ads, event_time, ten_minutes_in_epoch):
    return [
        ad
        for ad in ads
        if (
            ad["JobStartDate"] < event_time
            or ad["JobStartDate"] < event_time + ten_minutes_in_epoch
        )
        and ad["CompletionDate"] > event_time
    ]


headers, rows = get_ad_info(
    cms_pilot_ads, time_fmt_func=lambda x: strftime("%Y-%m-%d %H:%M:%S", localtime(x))
)


print("CMS Pilot Jobs")
print(tabulate.tabulate(rows, headers=headers, tablefmt="psql"))

print("Jobs with start time before event and end time after event")
filtered_ads = filter_ads_for_event(ads, event_time, ten_minutes_in_epoch)
headers, rows = get_ad_info(
    filtered_ads, time_fmt_func=lambda x: strftime("%Y-%m-%d %H:%M:%S", localtime(x))
)
print(tabulate.tabulate(rows, headers=headers, tablefmt="psql"))
