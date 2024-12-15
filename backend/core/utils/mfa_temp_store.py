
# # core/utils/mfa_temp_store.py
# import time
# from datetime import timedelta

# # Structure: pending_mfa[user_id] = (pin, expiry_timestamp)
# pending_mfa = {}

# def set_mfa_pin(user_id):
#     import random
#     pin = str(random.randint(1000,9999))
#     expiry = time.time() + 60  # 60 seconds from now
#     pending_mfa[user_id] = (pin, expiry)
#     return pin

# def verify_mfa_pin(user_id, pin):
#     if user_id not in pending_mfa:
#         return False
#     stored_pin, expiry = pending_mfa[user_id]
#     if time.time() > expiry:
#         # Expired
#         del pending_mfa[user_id]
#         return False
#     if stored_pin == pin:
#         # Valid
#         del pending_mfa[user_id]
#         return True
#     return False
