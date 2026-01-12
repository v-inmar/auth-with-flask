import random
import string
from app.utils.result_utils import Result, Ok, Error


def generate_random_string(min_length: int, max_length: int) -> Result[str, Exception]:
    try:
        # generate random length between min and max (inclusive)
        random_length = random.randint(min_length, max_length)

        # create a selection pool
        character_pool = string.ascii_lowercase + string.digits

        value = ''.join(random.choice(character_pool) for _ in range(random_length))

        return Ok(value)
    except Exception as e:
        return Error(e)
    

def hide_email_util(email: str) -> Result[str, Exception]:
    '''
    Returns a masked email address i.e. email@email.com to e***l@email.com

    @param email: str
    '''
    try:
        if "@" not in email:
            raise ValueError(f"email does not contain '@' symbol: {email}")
        
        if "." not in email:
            raise ValueError(f"email does not contain '.' symbol: {email}")
        

        split_email = email.split("@")
        if len(split_email) != 2:
            raise ValueError(f"split_email length is not equals to 2. Length: {len(split_email)}")
        
        if len(split_email[0].strip()) < 1:
            raise ValueError(f"split_email[0] stripped has invalid length. Length: {len(split_email[0].strip())}")
        
        name = split_email[0].strip()[0]
        if len(split_email[0].strip()) > 1:
            name += '*' * len(split_email[0].strip()[1:-1])
            name += split_email[0].strip()[-1]
        
        return Ok(name+"@"+split_email[1])
    except ValueError as e:
        return Error(e)