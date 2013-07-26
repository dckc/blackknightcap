'''notary -- notary/inspector capability pattern

based on `Vouching with Notary`__ pattern

__ http://wiki.erights.org/wiki/Walnut/Secure_Distributed_Computing/Capability_Patterns#Vouching_with_Notary.2FInspector

>>> WidgetInspectionService, getOrderFormFromBob = WidgetInc()
>>> inspector = WidgetInspectionService.getInspector()

>>> untrustedOrderForm = getOrderFormFromBob()
>>> trustedOrderForm = inspector.vouch(untrustedOrderForm)
>>> trustedOrderForm.agent()
'bob'

>>> untrustedOrderForm = getOrderFormFromBobsEvilTwin()
>>> trustedOrderForm = inspector.vouch(untrustedOrderForm)
Traceback (most recent call last):
  ...
NotVouchable

We have to be prepared for junk:

>>> inspector.vouch('random junk')
Traceback (most recent call last):
    ...
NotVouchable
'''

from encap import ESuite, slot, val, update


class Notary(ESuite):
    def __new__(cls, label=''):
        nonObject = object()
        vouchableObject = slot(nonObject)

        def __repr__(_):
            return 'Notary(%s)' % label

        class Inspector(ESuite):
            def __new__(cls):
                def __repr__(_):
                    return 'Inspector(%s)' % label

                def vouch(_, obj):
                    update(vouchableObject, nonObject)
                    try:
                        obj.startVouch()
                        if (val(vouchableObject) is nonObject):
                            # why return here but not below??
                            return unvouchedException(obj)
                        else:
                            vouchedObject = val(vouchableObject)
                            update(vouchableObject, nonObject)
                            return vouchedObject
                    except Exception as ex:
                        unvouchedException(obj, ex)

                return cls.make(__repr__, vouch)

        inspector = Inspector()

        def startVouch(_, obj):
            update(vouchableObject, obj)

        def getInspector(_):
            return inspector

        return cls.make(__repr__, startVouch, getInspector)


class NotVouchable(Exception):
    def __init__(self, obj, ex):
        self.obj = obj
        self.because = ex


def unvouchedException(obj, ex):
    raise NotVouchable(obj, ex)


def WidgetInc():  # pragma: nocover
    notary = Notary()

    class OrderForm(ESuite):
        def __new__(cls, salesPerson):

            def agent(_):
                return salesPerson

            def startVouch(orderForm):
                notary.startVouch(orderForm)

            return cls.make(startVouch, agent)

    class WidgetInspectionService(ESuite):
        '''publicly available inspector object
        (accessible through a uri posted on Widget Inc's web site) ' '''

        def __new__(cls):
            def getInspector(_):
                return notary.getInspector()
            return cls.make(getInspector)

    def getOrderFormFromBob():
        return OrderForm("bob")

    return WidgetInspectionService(), getOrderFormFromBob


def getOrderFormFromBobsEvilTwin():  # pragma: nocover
    """Bob's evil twinn """
    return ForgedOrderForm("bob")


class ForgedOrderForm(ESuite):  # pragma: nocover
    def __new__(cls, salesPerson):
        def agent(_):
            return salesPerson

        def startVouch():
            pass
        return cls.make(startVouch, agent)
