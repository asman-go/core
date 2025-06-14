import dns.resolver
from dns.rdatatype import RdataType
import typing

from ..models import Domain


class DomainResolveTask():

    @staticmethod
    def ip(domain: str, record_type: RdataType) -> typing.Sequence[str]:
        try:
            res = dns.resolver.resolve(domain, record_type)
            answer = res.response.answer
        except:
            return []

        res = []
        for ans in answer:
            res.extend(
                [x.address for x in ans.items.keys()]
            )

        return list(set(res))

    def _call(self, message: Domain):
        # TODO: дополнительно резолвить через выбранный DNS сервер (пока беру по умолчанию)

        ip_addresses = (
            DomainResolveTask.ip(message.domain, RdataType.A)
            +
            DomainResolveTask.ip(message.domain, RdataType.AAAA)
        )

        # Теперь надо как-то сохранить
        print('Message', self.config, message, ip_addresses)
