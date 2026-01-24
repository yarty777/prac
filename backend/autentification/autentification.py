from fastapi import APIRouter, HTTPException, Depends
from auth.jwt import create_access_token, verify_token
from auth.hash import hash_password, verify_password
