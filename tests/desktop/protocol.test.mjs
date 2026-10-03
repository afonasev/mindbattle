import { test } from "node:test";
import assert from "node:assert/strict";
import { createHandler } from "../../desktop/protocol.mjs";
test("fixed upstream, allowed headers, streaming and abort preservation", async () => {
  let received;
  const h = createHandler({
    directory: () => "/unused",
    origin: "https://game.example",
    fetcher: async (url, init) => {
      received = { url, init };
      return new Response(
        new ReadableStream({
          start(controller) {
            controller.enqueue(new TextEncoder().encode("data: hello\n\n"));
            controller.close();
          },
        }),
        { headers: { "content-type": "text/event-stream" } },
      );
    },
  });
  const request = new Request(
    "mindbattle://game/api/network/stream?code=1234",
    {
      headers: {
        origin: "mindbattle://game",
        authorization: "Bearer example",
        cookie: "private",
      },
    },
  );
  const response = await h(request);
  assert.equal(
    received.url,
    "https://game.example/api/network/stream?code=1234",
  );
  assert.equal(received.init.redirect, "error");
  assert.equal(received.init.headers.get("origin"), null);
  assert.equal(received.init.headers.get("cookie"), null);
  assert.equal(received.init.headers.get("authorization"), "Bearer example");
  assert.equal(received.init.signal, request.signal);
  assert.equal(await response.text(), "data: hello\n\n");
});
test("rejects unknown authority/API without making upstream calls", async () => {
  const h = createHandler({
    directory: () => "/unused",
    origin: "https://game.example",
    fetcher: () => {
      throw Error("must not fetch");
    },
  });
  assert.equal(
    (await h(new Request("mindbattle://evil/api/network/stream"))).status,
    403,
  );
  assert.equal(
    (await h(new Request("mindbattle://game/api/admin"))).status,
    404,
  );
  assert.equal(
    (await h(new Request("mindbattle://game/%2e%2e%2fsecret"))).status,
    404,
  );
});
