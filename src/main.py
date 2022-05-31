import json

from ibm_cloud_sdk_core import ApiException

from config_helper import get_user_management_service, get_account_id
from usage_report import get_account_summary, get_resource_usage
from vpc_infrastructure import get_vpc_infrastructure_data, print_vpc_infrastructure_data
from sheet import GoogleSheetEditor


# List users
def get_all_users():
    print("Listing Users")
    try:
        service = get_user_management_service()
        users = service.list_users(account_id=get_account_id()).get_result()['resources']
        print(json.dumps(users, indent=2))
    except ApiException as e:
        print("List Users failed with status code: {0} : {1}".format(e.code, e.message))



def get_old_instances_email_summary(oldInstancesSheet, allInstancesSheet, summarySheet):
    sheet_link = os.environ['SHEET_LINK']
    old_instances = prepare_old_instances_data(allInstancesSheet, oldInstancesSheet)
    if summarySheet is not None:
        try:
            total_ec2_deleted = summarySheet.read_custom('J1', 'J1')[0][0]
        except:
            total_ec2_deleted = None
    message = ""

if __name__ == '__main__':
    data = get_vpc_infrastructure_data()
    # print_vpc_infrastructure_data(data)
    print(data)

    # get_account_summary()
    # get_resource_usage()
    # get_all_users()

    #TODO:: Pick the sheetID from env variables
    sheet_id = "1VU6XfCxG_Q8nq9N-DX06rS618oP2pb1bdhvebV0fIic"

    allInstancesSheetName = "All Instances"
    allGatewaysSheetName = "All Gateways"
    allSubnetsSheetName = "All Subnets"
    allVPCsSheetName = "All VPCs"
    

    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allGatewaysSheet = GoogleSheetEditor(sheet_id, allGatewaysSheetName)
    allSubnetsSheet = GoogleSheetEditor(sheet_id, allSubnetsSheetName)
    allVPCsSheet = GoogleSheetEditor(sheet_id, allVPCsSheetName)

    
    print(allInstancesSheet.save_data_to_sheet(data['Instances']))
    print(allGatewaysSheet.save_data_to_sheet(data['Public Gateways']))
    print(allSubnetsSheet.save_data_to_sheet(data['Subnets']))
    print(allVPCsSheet.save_data_to_sheet(data['VPCs']))
 


