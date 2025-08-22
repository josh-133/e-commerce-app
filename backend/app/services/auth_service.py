class AuthService:
    async def login(self, username: str, password: str):
        # TODO check user in DB
        return {"message": f"User {username} logged in"}
    
    async def register(self, username: str, password: str):
        # TODO insert user in DB
        return {"message": f"User {username} registered"}