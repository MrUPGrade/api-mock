import falcon
import logging

class SimpleResponseProcessor:
    def process_response(self, response, response_data):
        logging.debug('RESPONSE: %s', response_data)
        response_body = response_data.get('body')

        if response_body:
            response.media = response_body

        status_code = response_data.get('status', '200')
        response.status = getattr(falcon, 'HTTP_%s' % status_code)

        headers = response_data.get('headers')
        if headers:
            for key, value in headers.items():
                response.append_header(key, value)
