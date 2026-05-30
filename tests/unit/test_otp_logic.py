import unittest
from app.services.otp_service import OTPService, otp_storage

class TestOTPService(unittest.TestCase):
    def setUp(self):
        self.service = OTPService.__new__(OTPService)
        otp_storage.clear()

    def test_generate_otp(self):
        otp = self.service.generate_otp()
        self.assertEqual(len(otp), 6)
        self.assertTrue(otp.isdigit())

    def test_store_and_verify_otp(self):
        identifier = "test@example.com"
        otp = "123456"
        self.service.store_otp(identifier, otp)
        
        # Test réussite
        self.assertTrue(self.service.verify_otp(identifier, otp))
        
        # Test OTP supprimé après usage
        self.assertFalse(self.service.verify_otp(identifier, otp))

    def test_verify_wrong_otp(self):
        identifier = "test@example.com"
        self.service.store_otp(identifier, "111111")
        self.assertFalse(self.service.verify_otp(identifier, "222222"))

if __name__ == '__main__':
    unittest.main()
