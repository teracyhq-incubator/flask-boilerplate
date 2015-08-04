# -*- coding: utf-8 -*-

"""tests for app.pagination"""

from mock import patch, MagicMock, call

from tests.unit import UnitTestCase


class CursorPaginationTestCase(UnitTestCase):

    def test_init(self):
        from app.pagination import CursorPagination

        cursor_pagination = CursorPagination(MagicMock())

        self.assertIsNotNone(cursor_pagination)


class TimePaginationTestCase(UnitTestCase):

    def test_init(self):
        from app.pagination import TimePagination

        time_pagination = TimePagination(MagicMock())

        self.assertIsNotNone(time_pagination)


class OffsetPaginationTestCase(UnitTestCase):

    def setUp(self):
        self.current_app_patcher = patch('app.pagination.current_app')
        self.mock_current_app = self.current_app_patcher.start()

    def tearDown(self):
        self.mock_current_app.reset()
        del self.mock_current_app
        self.current_app_patcher.stop()
        del self.current_app_patcher

    def test_init_invalid(self):
        self.mock_current_app.config.get.return_value = 30
        mock_query = MagicMock()

        from app.pagination import OffsetPagination

        with self.assertRaises(ValueError) as ve:
            OffsetPagination(mock_query, -2)
        self.assertEqual(ve.exception.message, 'offset is negative(-2), should be positive or zero')

        with self.assertRaises(ValueError) as ve:
            OffsetPagination(mock_query, limit=-3)
        self.assertEqual(ve.exception.message, 'limit is negative(-3), should be positive')

        self.assertEqual(self.mock_current_app.config.get.call_count, 2)

    def test_init_default(self):
        self.mock_current_app.config.get.return_value = 30
        mock_query = MagicMock()
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 15
        mock_query.all.return_value = ['hi']

        from app.pagination import OffsetPagination

        offset_pagination = OffsetPagination(mock_query)

        self.assertEqual(offset_pagination.offset, 0)
        self.assertEqual(offset_pagination.limit, 30)
        self.assertEqual(offset_pagination.count, 15)
        self.assertEqual(offset_pagination.data, ['hi'])

        self.mock_current_app.config.get.assert_called_once_with('PAGINATION_LIMIT', 25)
        mock_query.count.assert_called_once_with()
        mock_query.all.assert_called_once_with()
        mock_query.offset.assert_has_calls([call(None), call(0)])
        mock_query.limit.assert_has_calls([call(None), call(30)])

    def test_init_full(self):
        self.mock_current_app.config.get.return_value = 15
        mock_query = MagicMock()
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 3
        mock_query.all.return_value = ['hi', 'there']

        from app.pagination import OffsetPagination

        offset_pagination = OffsetPagination(mock_query, 1, 20)

        self.assertEqual(offset_pagination.offset, 1)
        self.assertEqual(offset_pagination.limit, 15)
        self.assertEqual(offset_pagination.count, 3)
        self.assertEqual(offset_pagination.data, ['hi', 'there'])

        mock_query.count.assert_called_once_with()
        mock_query.all.assert_called_once_with()
        mock_query.offset.assert_has_calls([call(None), call(1)])
        mock_query.limit.assert_has_calls([call(None), call(15)])

    def test_has_prev(self):
        self.mock_current_app.config.get.return_value = 25
        mock_query = MagicMock()

        from app.pagination import OffsetPagination

        offset_pagination = OffsetPagination(mock_query)

        self.assertFalse(offset_pagination.has_prev)

        offset_pagination = OffsetPagination(mock_query, offset=5, limit=5)

        self.assertTrue(offset_pagination.has_prev)

    def test_has_next(self):
        self.mock_current_app.config.get.return_value = 25
        mock_query = MagicMock()
        mock_query.offset.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.count.return_value = 10

        from app.pagination import OffsetPagination

        offset_pagination = OffsetPagination(mock_query)

        self.assertFalse(offset_pagination.has_next)

        offset_pagination = OffsetPagination(mock_query, offset=0, limit=6)

        self.assertTrue(offset_pagination.has_next)

    def test_prev_url_none(self):
        self.mock_current_app.config.get.return_value = 25

        from app.pagination import OffsetPagination
        mock_query = MagicMock()

        offset_pagination = OffsetPagination(mock_query, offset=4, limit=5)

        self.assertIsNone(offset_pagination.prev_url)

    def test_prev_url_exists(self):
        self.mock_current_app.config.get.return_value = 25

        from app.pagination import OffsetPagination
        mock_query = MagicMock()

        offset_pagination = OffsetPagination(mock_query, offset=6, limit=5)
        self.assertEqual(offset_pagination.offset, 6)
        self.assertEqual(offset_pagination.limit, 5)
        self.assertTrue(offset_pagination.has_prev)

        with patch.object(OffsetPagination, 'page_url', return_value='http://') as mock_page_url:
            offset_pagination = OffsetPagination(mock_query, offset=6, limit=5)
            self.assertTrue(offset_pagination.has_prev)
            self.assertEqual(offset_pagination.prev_url, 'http://')
            mock_page_url.assert_called_once_with(1, 5)

    def test_next_url_none(self):
        self.mock_current_app.config.get.return_value = 25

        from app.pagination import OffsetPagination
        mock_query = MagicMock()
        mock_query.offset.return_value.limit.return_value.count.return_value = 15

        offset_pagination = OffsetPagination(mock_query, offset=10, limit=5)

        self.assertIsNone(offset_pagination.next_url)

        with patch.object(OffsetPagination, 'page_url', return_value='http://') as mock_page_url:
            offset_pagination = OffsetPagination(mock_query, offset=6, limit=5)
            self.assertTrue(offset_pagination.has_next)
            self.assertEqual(offset_pagination.next_url, 'http://')
            mock_page_url.assert_called_once_with(11, 5)

    @patch('app.pagination.url_for')
    @patch('app.pagination.request')
    def test_page_url(self, mock_request, mock_url_for):
        mock_request.view_args.copy.return_value = {}
        mock_request.endpoint = 'users'
        mock_url_for.return_value = 'http://example.com/api/v1.0/users?offset=0&limit=20'

        from app.pagination import OffsetPagination

        self.assertTrue(callable(OffsetPagination.page_url))

        url = OffsetPagination.page_url(0, 20)

        self.assertEqual(url, 'http://example.com/api/v1.0/users?offset=0&limit=20')
        mock_request.view_args.copy.assert_called_once_with()
        mock_request.values.to_dict.assert_called_once_with()
        mock_url_for.assert_called_once_with('users', _external=True, **{'offset': 0, 'limit': 20})
