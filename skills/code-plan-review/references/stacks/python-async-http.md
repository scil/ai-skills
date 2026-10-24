# Python async HTTP (anyio, httpx / httpx2, httpcore)

Load when a manifest holds `anyio`, `httpx` or `httpx2` (directly or through an SDK built on them, such as `anthropic` ≥ 1), or when the plan puts a socket guard, a proxy or a retry layer under such a client. Checked against anyio 4.x, httpx2 2.16, httpcore2 (Python 3.12, Windows proactor loop), 2026-10-24.

## A3.11

- **Shows up as:** a policy refusal raised below the HTTP client — a socket guard's exception, a firewall hook — is a subclass of `OSError` (as such guards usually are, to look like a failed connect). anyio's `connect_tcp` catches every `OSError` from its connection attempts and raises its own "All connection attempts failed"; httpx maps that to `ConnectError`. The retry layer above classifies `ConnectError` as transient and sends the refused request again, and the caller finally sees "could not connect" instead of "refused".
- **Look for:** a retry or fallback that branches on `ConnectError` / `ConnectTimeout`, in a process that also installs a socket guard or patches `socket.connect` / `loop.sock_connect`; tests of the guard that call `socket.create_connection` directly (they see the guard's own exception) and none that go through an `AsyncClient`.
- **Fix:** before classifying a connect error, walk its `__cause__`, `__context__` and any `ExceptionGroup.exceptions` for the guard's exception type, and treat a hit as a refusal (no retry, the guard's reason passed on); a test sends through the real async client stack to a refused address and asserts one attempt.
