from rest_framework.throttling import SimpleRateThrottle


class SubscriptionTierThrottle(SimpleRateThrottle):
    scope = 'tier'

    def get_cache_key(self, request, view):
        """
        Har bir userni qanday 'tanish'?

        Cache — bu xotira daftari:
          throttle_tier_1 → Ali    → 45 ta so'rov
          throttle_tier_2 → Vali   → 12 ta so'rov
          throttle_tier_3 → Sardor → 99 ta so'rov

        None qaytarsa → bu klassni o'tkazib yubor
        """
        if not request.user.is_authenticated:
            return None  # ← anonim userni boshqa klass cheklaydi

        return f'throttle_tier_{request.user.id}'

    def allow_request(self, request, view):
        """
        True  → ✅ ruxsat bor, davom et
        False → ❌ 429 qaytariladi
        """
        if not request.user.is_authenticated:
            return True  # ← bu klass anonim userni tekshirmaydi

        # Obuna darajasiga qarab tezlik belgilash
        # Darsda: is_staff orqali test qiling
        if request.user.is_staff:
            self.rate = '100/min'  # staff → cheksiz deyarli
        elif request.user.is_authenticated:
            self.rate = '10/min'  # oddiy user → kamroq
        else:
            self.rate = '5/min'

        # '10/min' → (10, 60) ga o'girish
        self.num_requests, self.duration = self.parse_rate(self.rate)

        # Asosiy tekshiruv: nechta yuborgan?
        return super().allow_request(request, view)
