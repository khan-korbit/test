import boto3
import pandas as pd

ec2 = boto3.resource('ec2')

data = []

for instance in ec2.instances.all():
    for sg in instance.security_groups:
        # 보안 그룹의 모든 인바운드 규칙 출력
        security_group = ec2.SecurityGroup(sg['GroupId'])
        for rule in security_group.ip_permissions:
            from_port = rule.get('FromPort', 'None')  # 'FromPort'가 없으면 'None'을 반환합니다.
            to_port = rule.get('ToPort', 'None')  # 'ToPort'가 없으면 'None'을 반환합니다.
            for ip_range in rule['IpRanges']:
                # 데이터를 리스트에 추가
                data.append([instance.id, from_port, to_port, ip_range["CidrIp"]])

# pandas DataFrame 생성
df = pd.DataFrame(data, columns=['Instance ID', 'From Port', 'To Port', 'IP Range'])

# DataFrame을 Excel 파일로 저장
df.to_excel('aws_ec2_ports.xlsx', index=False)
