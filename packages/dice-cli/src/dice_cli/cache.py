from diskcache import FanoutCache

admin_cache = FanoutCache("~/.dice_admin_cache", shards=4, timeout=1)
user_cache = FanoutCache("~/.dice_user_cache", shards=4, timeout=1)
