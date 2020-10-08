import json
import boto3
import csv
import operator
from datetime import datetime, date, timedelta

setMinutes = 10              # 調査する分数
period = setMinutes * 60     # 調査期間となる秒数
instanceId = "i-xxxxxxxxxxx" #対象のEC2インスタンス

now = datetime.now()
startTime = now - timedelta(minutes=setMinutes)
endTime = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
startTime = datetime.strftime(startTime, '%Y-%m-%d %H:%M:%S')

def lambda_handler(event, context):
    all_metrics_list = [
        {
        'NameSpaceHeader' : 'AWS/',
        'NameSpace' : 'EC2',
        'MetricName':'CPUUtilization',
        'Dimensions':[{"Name" : "InstanceId","Value" : instanceId}],
        'Statistics' : 'Average'
        }
    ]

    for target in all_metrics_list:
        #メトリクス取得
        logs = getMetricStatistics(target)


    return {
        'statusCode': 200,
        'body': json.dumps(logs, default=support_datetime_default)
    }


def getMetricStatistics(target_dict):
    cloudwatch = boto3.client('cloudwatch', region_name='ap-northeast-1')

    logs = cloudwatch.get_metric_statistics(
                                Namespace=target_dict["NameSpaceHeader"] + target_dict["NameSpace"],
                                MetricName=target_dict["MetricName"],
                                Dimensions=target_dict["Dimensions"],
                                StartTime=startTime,
                                EndTime=endTime,
                                Period=period,
                                Statistics=[target_dict["Statistics"]]
                                )
    return logs
    

def support_datetime_default(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(repr(o) + " is not JSON serializable")
