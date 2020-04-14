import QualysAPI
import QualysSubscriptionProcessor


def testSubscription(source_api: QualysAPI.QualysAPI, target_api: QualysAPI.QualysAPI):
    configxml = QualysSubscriptionProcessor.exportSubscriptionConfig(api=source_api)
    response = QualysSubscriptionProcessor.importSubscriptionConfig(api=target_api, configxml=configxml)
    return response
