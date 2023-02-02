from dotenv import load_dotenv
import os 

load_dotenv()
schema_version = os.getenv("PERMIFY_SCHEMA_VERSION")

PERMIFY_BASE_URL = "http://localhost:3476"
PERMIFY_RELATIONAL_TUPLE_URL = f"{PERMIFY_BASE_URL}/v1/tenants/t1/relationships/write"
PERMIFY_CHECK_PERMISSION_URL = f"{PERMIFY_BASE_URL}/v1/tenants/t1/permissions/check"
