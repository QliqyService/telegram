from fastapi.responses import StreamingResponse
from fastapi import status
from app.routers.api import Router
from app.schemas.account_linking import TGRPCRequest, TGRPCResponse

router = Router(
    name="Telegram Bot",
    description="Endpoints for telegram bot and account linking"
)


@router.post("/link_accounts",
             status_code=status.HTTP_200_OK,
             response_model=TGRPCResponse)
def link_accounts(payload: TGRPCRequest):
    """
     Links accounts
    Args:
        payload (Account_linking_Request): Body of HTTP-request:
        - code (str)
        - telegram_id (str)
        - ok (str)

    Returns:
        StreamingResponse: Streaming HTTP-response
        - code (str)
        - telegram_id (str)
        - ok (str)
    """
    pass
    #TODO
