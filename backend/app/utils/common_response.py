# from fastapi.responses import JSONResponse

# def success_response(data=None, message="Success", code=200):
#     return JSONResponse(
#         status_code=code,
#         content={
#             "response_status": True,
#             "status_code": code,
#             "message": message,
#             "source_output": data,
#         },
#     )

# def error_response(message="Error", code=400):
#     return JSONResponse(
#         status_code=code,
#         content={
#             "response_status": False,
#             "status_code": code,
#             "message": message,
#             "source_output": None,
#         },
#     )
