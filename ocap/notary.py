'''

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

from ocap_file import edef


def makeNotary(label=''):
    nonObject = object()
    vouchableObject = slot(nonObject)

    def vouch(obj):
        update(vouchableObject, nonObject)
        try:
            obj.startVouch()
            if (value(vouchableObject) is nonObject):
                # why return here but not below??
                return unvouchedException(obj)
            else:
                vouchedObject = value(vouchableObject)
                update(vouchableObject, nonObject)
                return vouchedObject
        except Exception as ex:
            unvouchedException(obj, ex)

    def vouch_repr():
        return 'Inspector(%s)' % label

    inspector = edef(vouch, __repr__=vouch_repr)

    def startVouch(obj):
        update(vouchableObject, obj)

    def getInspector():
        return inspector

    def __repr__():
        return 'Notary(%s)' % label

    return edef(startVouch, getInspector, __repr__)


def slot(init=None):
    return [init]


def value(slot):
    return slot[0]


def update(slot, val):
    slot[0] = val


class NotVouchable(Exception):
    def __init__(self, obj, ex):
        self.obj = obj
        self.because = ex


def unvouchedException(obj, ex):
    raise NotVouchable(obj, ex)


def WidgetInc():  # pragma: nocover
    notary = makeNotary()

    def makeOrderForm(salesPerson):
        orderForm = None  # forward reference

        def agent():
            return salesPerson

        def startVouch():
            notary.startVouch(orderForm)

        orderForm = edef(startVouch, agent)
        return orderForm

    def _s():
        def getInspector():
            return notary.getInspector()
        return edef(getInspector)

    '''publicly available inspector object
    (accessible through a uri posted on Widget Inc's web site) ' '''
    WidgetInspectionService = _s()

    def getOrderFormFromBob():
        return makeOrderForm("bob")

    return WidgetInspectionService, getOrderFormFromBob


def getOrderFormFromBobsEvilTwin():  # pragma: nocover
    """Bob's evil twinn """
    return forgeOrderForm("bob")


def forgeOrderForm(salesPerson):  # pragma: nocover
    orderForm = None  # forward reference

    def agent():
        return salesPerson

    def startVouch():
        pass
    orderForm = edef(startVouch, agent)
    return orderForm
