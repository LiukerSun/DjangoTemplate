from rest_framework.renderers import JSONRenderer


class ApiResponseRenderer(JSONRenderer):
    """自定义渲染器，统一接口返回格式

    最终返回结构：
    {
        "status": "success" | "error",
        "message": "提示信息",
        "data": 任意数据或 None
    }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 如果没有 renderer_context，直接使用父类渲染
        if renderer_context is None:
            return super().render(data, accepted_media_type, renderer_context)

        response = renderer_context.get("response")

        # 若 data 已经符合统一格式，则直接返回
        if isinstance(data, dict) and {
            "status",
            "message",
            "data",
        }.issubset(data.keys()):
            return super().render(data, accepted_media_type, renderer_context)

        status_code = getattr(response, "status_code", 200)
        # 根据状态码判定成功或失败
        status_label = "success" if status_code < 400 else "error"
        # 默认 message
        default_message = "操作成功" if status_label == "success" else "请求错误"

        unified_data = {
            "status": status_label,
            "message": default_message,
            "data": data if status_label == "success" else None,
        }
        return super().render(unified_data, accepted_media_type, renderer_context) 