// Runs before the static site: one canonical address for Google.
// http:// and the bare domain (valeriorosponi.com) answer with a permanent redirect to
// https://www.valeriorosponi.com, same path and query; everything else is the built site.
const CANONICAL_HOST = 'www.valeriorosponi.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const isSiteHost = url.hostname === CANONICAL_HOST || url.hostname === 'valeriorosponi.com';
    if (isSiteHost && (url.hostname !== CANONICAL_HOST || url.protocol === 'http:')) {
      url.hostname = CANONICAL_HOST;
      url.protocol = 'https:';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
