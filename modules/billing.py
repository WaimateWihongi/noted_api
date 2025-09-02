from .base import Base

class Billing(Base):
    def __init__(self):
        super().__init__()
    
    def get_billing_info(self):
        """ Get information for billing """
        response = self.post("graphql", {
            "query": "\n    query organisationWithSubscription($id: Long!) {\n  organisationWithSubscription(id: $id) {\n    organisation {\n      featurePackage {\n        id\n        name\n      }\n    }\n    addons {\n      id\n      name\n      description\n      permissionName\n      enabled\n      addOn\n      unitPrice\n      totalPrice\n      billableUsers\n      chargeType\n      chargePeriod\n    }\n    subscription {\n      id\n      planPerUnitCosts\n      planName\n      planId\n      currencyCode\n      monthlyCost\n      totalBillableUsers\n      chargeModel\n    }\n  }\n}\n    ",
            "variables": {
                "id": 594
            }
        })
        return response.json()