File "/mount/src/my-ai-app/ai.app.py", line 17, in <module>
    response = model.generate_content(prompt)
File "/home/adminuser/venv/lib/python3.13/site-packages/google/generativeai/generative_models.py", line 331, in generate_content
    response = self._client.generate_content(
        request,
        **request_options,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/google/ai/generativelanguage_v1beta/services/generative_service/client.py", line 835, in generate_content
    response = rpc(
        request,
    ...<2 lines>...
        metadata=metadata,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/gapic_v1/method.py", line 128, in __call__
    return wrapped_func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/retry/retry_unary.py", line 294, in retry_wrapped_func
    return retry_target(
        target,
    ...<3 lines>...
        on_error=on_error,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/retry/retry_unary.py", line 156, in retry_target
    next_sleep = _retry_error_helper(
        exc,
    ...<6 lines>...
        timeout,
    )
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/retry/retry_base.py", line 216, in _retry_error_helper
    raise final_exc from source_exc
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/retry/retry_unary.py", line 147, in retry_target
    result = target()
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/timeout.py", line 130, in func_with_timeout
    return func(*args, **kwargs)
File "/home/adminuser/venv/lib/python3.13/site-packages/google/api_core/grpc_helpers.py", line 57, in error_remapped_callable
    raise exceptions.from_grpc_error(exc) from exc
