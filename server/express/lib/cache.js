export default function (req, res, next) {
  // Keep cache for 5 minutes (in seconds)
  const period = 60 * 5;

  req.method == "GET"
    ? res.set("Cache-control", `public, max-age=${period}`)
    : res.set("Cache-control", `no-store`);
  next();
}
