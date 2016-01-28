import json
from datetime import (datetime, timedelta)
from flask import url_for

from app.models import (VerifyCode)
from app import db
from tests import create_authorization_header


def test_user_verify_code_sms(notify_api,
                              notify_db,
                              notify_db_session,
                              sample_sms_code):
    """
    Tests POST endpoint '/<user_id>/verify/code'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            assert not VerifyCode.query.first().code_used
            data = json.dumps({
                'code_type': sample_sms_code.code_type,
                'code': sample_sms_code.txt_code})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_code', user_id=sample_sms_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_code', user_id=sample_sms_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 204
            assert VerifyCode.query.first().code_used


def test_user_verify_code_sms_missing_code(notify_api,
                                           notify_db,
                                           notify_db_session,
                                           sample_sms_code):
    """
    Tests POST endpoint '/<user_id>/verify/code'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            assert not VerifyCode.query.first().code_used
            data = json.dumps({'code_type': sample_sms_code.code_type})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_code', user_id=sample_sms_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_code', user_id=sample_sms_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 400
            assert not VerifyCode.query.first().code_used


def test_user_verify_code_email(notify_api,
                                notify_db,
                                notify_db_session,
                                sample_email_code):
    """
    Tests POST endpoint '/<user_id>/verify/code'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            assert not VerifyCode.query.first().code_used
            data = json.dumps({
                'code_type': sample_email_code.code_type,
                'code': sample_email_code.txt_code})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 204
            assert VerifyCode.query.first().code_used


def test_user_verify_code_email_bad_code(notify_api,
                                         notify_db,
                                         notify_db_session,
                                         sample_email_code):
    """
    Tests POST endpoint '/<user_id>/verify/code'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            assert not VerifyCode.query.first().code_used
            data = json.dumps({
                'code_type': sample_email_code.code_type,
                'code': "blah"})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 404
            assert not VerifyCode.query.first().code_used


def test_user_verify_code_email_expired_code(notify_api,
                                             notify_db,
                                             notify_db_session,
                                             sample_email_code):
    """
    Tests POST endpoint '/<user_id>/verify/code'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            assert not VerifyCode.query.first().code_used
            sample_email_code.expiry_datetime = (
                datetime.now() - timedelta(hours=1))
            db.session.add(sample_email_code)
            db.session.commit()
            data = json.dumps({
                'code_type': sample_email_code.code_type,
                'code': sample_email_code.txt_code})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_code', user_id=sample_email_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 400
            assert not VerifyCode.query.first().code_used


def test_user_verify_password(notify_api,
                              notify_db,
                              notify_db_session,
                              sample_user):
    """
    Tests POST endpoint '/<user_id>/verify/password'
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'password': 'password'})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_password', user_id=sample_user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_password', user_id=sample_user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 204


def test_user_verify_password_invalid_password(notify_api,
                                               notify_db,
                                               notify_db_session,
                                               sample_user):
    """
    Tests POST endpoint '/<user_id>/verify/password' invalid endpoint.
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'password': 'bad password'})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_password', user_id=sample_user.id),
                method='POST',
                request_body=data)

            assert sample_user.failed_login_count == 0

            resp = client.post(
                url_for('user.verify_user_password', user_id=sample_user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 400
            json_resp = json.loads(resp.get_data(as_text=True))
            assert 'Incorrect password' in json_resp['message']['password']
            assert sample_user.failed_login_count == 1


def test_user_verify_password_valid_password_resets_failed_logins(notify_api,
                                                                  notify_db,
                                                                  notify_db_session,
                                                                  sample_user):

    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'password': 'bad password'})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_password', user_id=sample_user.id),
                method='POST',
                request_body=data)

            assert sample_user.failed_login_count == 0

            resp = client.post(
                url_for('user.verify_user_password', user_id=sample_user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 400
            json_resp = json.loads(resp.get_data(as_text=True))
            assert 'Incorrect password' in json_resp['message']['password']

            assert sample_user.failed_login_count == 1

            data = json.dumps({'password': 'password'})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_password', user_id=sample_user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_password', user_id=sample_user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])

            assert resp.status_code == 204
            assert sample_user.failed_login_count == 0


def test_user_verify_password_missing_password(notify_api,
                                               notify_db,
                                               notify_db_session,
                                               sample_user):
    """
    Tests POST endpoint '/<user_id>/verify/password' missing password.
    """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'bingo': 'bongo'})
            auth_header = create_authorization_header(
                path=url_for('user.verify_user_password', user_id=sample_user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.verify_user_password', user_id=sample_user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 400
            json_resp = json.loads(resp.get_data(as_text=True))
            assert 'Required field missing data' in json_resp['message']['password']


def test_send_user_code_for_sms(notify_api,
                                notify_db,
                                notify_db_session,
                                sample_sms_code,
                                mock_notify_client_send_sms,
                                mock_secret_code):
    """
   Tests POST endpoint '/<user_id>/code' successful sms
   """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'code_type': 'sms'})
            auth_header = create_authorization_header(
                path=url_for('user.send_user_code', user_id=sample_sms_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.send_user_code', user_id=sample_sms_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])

            assert resp.status_code == 204
            mock_notify_client_send_sms.assert_called_once_with(mobile_number=sample_sms_code.user.mobile_number,
                                                                message='11111')


def test_send_user_code_for_sms_with_optional_to_field(notify_api,
                                                       notify_db,
                                                       notify_db_session,
                                                       sample_sms_code,
                                                       mock_notify_client_send_sms,
                                                       mock_secret_code):
    """
   Tests POST endpoint '/<user_id>/code' successful sms with optional to field
   """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'code_type': 'sms', 'to': '+441119876757'})
            auth_header = create_authorization_header(
                path=url_for('user.send_user_code', user_id=sample_sms_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.send_user_code', user_id=sample_sms_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])

            assert resp.status_code == 204
            mock_notify_client_send_sms.assert_called_once_with(mobile_number='+441119876757',
                                                                message='11111')


def test_send_user_code_for_email(notify_api,
                                  notify_db,
                                  notify_db_session,
                                  sample_email_code,
                                  mock_notify_client_send_email,
                                  mock_secret_code):
    """
   Tests POST endpoint '/<user_id>/code' successful email
   """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'code_type': 'email'})
            auth_header = create_authorization_header(
                path=url_for('user.send_user_code', user_id=sample_email_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.send_user_code', user_id=sample_email_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 204
            mock_notify_client_send_email.assert_called_once_with(sample_email_code.user.email_address,
                                                                  '11111',
                                                                  'notify@digital.cabinet-office.gov.uk',
                                                                  'Verification code')


def test_send_user_code_for_email_uses_optional_to_field(notify_api,
                                                         notify_db,
                                                         notify_db_session,
                                                         sample_email_code,
                                                         mock_notify_client_send_email,
                                                         mock_secret_code):
    """
   Tests POST endpoint '/<user_id>/code' successful email with included in body
   """
    with notify_api.test_request_context():
        with notify_api.test_client() as client:
            data = json.dumps({'code_type': 'email', 'to': 'different@email.gov.uk'})
            auth_header = create_authorization_header(
                path=url_for('user.send_user_code', user_id=sample_email_code.user.id),
                method='POST',
                request_body=data)
            resp = client.post(
                url_for('user.send_user_code', user_id=sample_email_code.user.id),
                data=data,
                headers=[('Content-Type', 'application/json'), auth_header])
            assert resp.status_code == 204
            mock_notify_client_send_email.assert_called_once_with('different@email.gov.uk',
                                                                  '11111',
                                                                  'notify@digital.cabinet-office.gov.uk',
                                                                  'Verification code')