def checkout_item(catalog_db, item_id: str, user_id: str) -> tuple[bool, str]:
    """
    :param item_id: uuid
    :param user_id: uuid
    """
    # Look up item and determine availability
    return catalog_db.try_checkout(item_id, user_id)
