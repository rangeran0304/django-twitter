
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from accounts.models import UserProfile
from testing.testcase import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'
USERPROFILE_URL = '/api/profiles/{}/'


class AccountApiTests(TestCase):

    def setUp(self):
        # 这个函数会在每个 test function 执行的时候被执行
        self.client = APIClient()
        self.user = self.createUser(
            username='test123',
            email='test123@test.com',
            password='123456789',
        )

    def createUser(self, username, email, password):
        # 不能写成 User.objects.create()
        # 因为 password 需要被加密, username 和 email 需要进行一些 normalize 处理
        return User.objects.create_user(username, email, password)

    def test_login(self):
        # 每个测试函数必须以 test_ 开头，才会被自动调用进行测试
        # 测试必须用 post 而不是 get
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': '123456789',
        })
        # 登陆失败，http status code 返回 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)

        # 用了 post 但是密码错了
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 400)

        # 验证还没有登录
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['if_logged_in'], False)
        # 用正确的密码
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': '123456789',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['username'], 'test123')
        # 验证已经登录了
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['if_logged_in'], True)

    def test_logout(self):
        # 先登录
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': '123456789',
        })
        # 验证用户已经登录
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['if_logged_in'], True)

        # 测试必须用 post
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        # 改用 post 成功 logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code, 200)
        # 验证用户已经登出
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['if_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': '123456789',
        }
        # 测试 get 请求失败
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # 测试错误的邮箱
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': '123456789',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # 测试密码太短
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': '123',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # 测试用户名太长
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong',
            'email': 'someone@jiuzhang.com',
            'password': 'any password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # 成功注册
        self.assertEqual(UserProfile.objects.count(),0)
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        self.assertEqual(UserProfile.objects.count(), 1)
        # 验证用户已经登入
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['if_logged_in'], True)

class userprofileapitests(TestCase):
    def test_update(self):
        testuser,testuserclient = self.create_user_and_client('testuesr')
        profile = testuser.profile
        profile.nickname = 'oldname'
        profile.save()
        testuser2,testuser2client = self.create_user_and_client('testuser2')
        url =USERPROFILE_URL.format(profile.id)
        # the profile can only be updated by the object owner
        response = testuser2client.put(url,{
            'nickname':'newname'
        })
        self.assertEqual(response.status_code,403)
        # test update nickname
        response = testuserclient.put(url, {
            'nickname': 'newname'
        })
        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertEqual(profile.nickname, 'newname')
        # test update avatar
        response = testuserclient.put(url, {
            'avatar': SimpleUploadedFile(
                name='my-avatar.jpg',
                content=str.encode('a fake image'),
                content_type='image/jpeg',
            ),
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual('my-avatar' in response.data['avatar'], True)
        p.refresh_from_db()
        self.assertIsNotNone(profile.avatar)
