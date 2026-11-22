"""展示缓存失效规则；不是完整自回归 attention/KV-cache。"""
import hashlib
import json


def cache_key(context):
    # context 应包含 model/adapter/prompt/reference/history/noise/position/mask 版本。
    encoded = json.dumps(context, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(encoded.encode()).hexdigest()


class FixedContextCache:
    def __init__(self):
        self.key, self.layers = None, {}

    def switch_context(self, context):
        key = cache_key(context)
        if key != self.key:
            self.layers.clear()  # prompt/timestep/历史变了就不能复用旧状态。
            self.key = key

    def remember(self, layer_id, k, v):
        self.layers[layer_id] = (k.detach(), v.detach())


# 仅适用于已固定条件的推理缓存；当前正在去噪的 token 仍需重算 Q/K/V。
