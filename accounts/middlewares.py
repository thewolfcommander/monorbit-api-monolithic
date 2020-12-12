import time


class StatsMiddleware:
    """
    Middleware to calculate response time for the request made on the server
    """
    def __init__(self, get_response):
        """
        Initializing the response state
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Call the request response calculator
        """
        # Recording the time before the request
        start_time = time.time()

        # Getting the response for the request
        response = self.get_response(request)

        # Calculating the total ltime taken by the request. Current time - time at which request started
        duration = time.time() - start_time

        # Add the header. Or do other things, my use case is to send a monitoring metric
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        print("Response Time for request - {} ms".format(str(int(duration * 1000))))
        return response