// Idempotent single-node replica set bootstrap, run as the mongo container healthcheck.
// Exit 0 only when this node is PRIMARY (so dependants can use service_healthy).
// Member host is "mongo:27017" so containers on the "stackshop" network can use
// mongodb://mongo:27017/?replicaSet=rs0 ; host tools use ?directConnection=true.
const HOST = 'mongo:27017';
const cfg = db.getSiblingDB('local').getCollection('system.replset').findOne();
if (!cfg) {
  rs.initiate({ _id: 'rs0', members: [{ _id: 0, host: HOST }] });
} else if (cfg.members.length !== 1 || cfg.members[0].host !== HOST) {
  // Volume was initiated with a different host name: force-fix it (single-node, safe).
  cfg.members = [Object.assign(cfg.members[0], { host: HOST })];
  cfg.version += 1;
  rs.reconfig(cfg, { force: true });
}
if (!db.hello().isWritablePrimary) {
  quit(1);
}
// Materialise the catalog database (idempotent).
const cat = db.getSiblingDB('catalog');
if (!cat.getCollectionNames().includes('_init')) {
  cat.createCollection('_init');
}
quit(0);
