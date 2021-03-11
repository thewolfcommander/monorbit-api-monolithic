from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAA2K1CcvY:APA91bETip6BmNQufvA-4jk6vcxbj1voOTVyhMVAWczBt9xUuwire9PDNaQEzZ8h1JdK0D2PrMRftpclJ2NSdnAw06Re2aFagmh3C6IBjx8_QDAT0ykSbuEjEApq6Y7bMtqW1DbVB11E")

def single_notification(registration_id,message_title,message_body):
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    return result


def multiple_device_notification(registration_ids,message_title,message_body):
    """
    registration_ids - List
    """
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    return result
