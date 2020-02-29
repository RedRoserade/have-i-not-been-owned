import time

from have_i_not_been_owned.celery.tasks import load_data_breach


def test_load_data_breach():
    start = time.monotonic()

    url = 'http://localhost:9000/test/neopets.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ACCESS%2F20200229%2F%2Fs3%2Faws4_request&X-Amz-Date=20200229T152841Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=451c07ec0ec21cb161c6916f2b2815bcbcbe85cb4c4c3b36f0d5e02834165a6d'

    result = load_data_breach(source={'url': url}, breach={'id': 'neopets'})

    end = time.monotonic()

    print(result)

    print(end - start)


if __name__ == '__main__':
    test_load_data_breach()
