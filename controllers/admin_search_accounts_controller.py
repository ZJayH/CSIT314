# controllers/admin_search_accounts_controller.py

from entities.account_entity import AccountEntity
from sqlalchemy import or_

class AdminSearchAccountsController:
    def handle(self, keyword: str) -> list[AccountEntity]:
        """
        Return accounts where name or email contains the keyword (case‐insensitive).
        """
        return AccountEntity.search(keyword)

