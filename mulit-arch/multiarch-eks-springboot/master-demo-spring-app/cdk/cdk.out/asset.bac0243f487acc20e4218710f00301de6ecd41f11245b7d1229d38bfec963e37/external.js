"use strict";
/* istanbul ignore file */
Object.defineProperty(exports, "__esModule", { value: true });
exports.external = void 0;
const tls = require("tls");
const url = require("url");
// eslint-disable-next-line import/no-extraneous-dependencies
const aws = require("aws-sdk");
let client;
function iam() {
    if (!client) {
        client = new aws.IAM();
    }
    return client;
}
function defaultLogger(fmt, ...args) {
    // eslint-disable-next-line no-console
    console.log(fmt, ...args);
}
/**
 * Downloads the CA thumbprint from the issuer URL
 */
async function downloadThumbprint(issuerUrl) {
    exports.external.log(`downloading certificate authority thumbprint for ${issuerUrl}`);
    return new Promise((ok, ko) => {
        const purl = url.parse(issuerUrl);
        const port = purl.port ? parseInt(purl.port, 10) : 443;
        if (!purl.host) {
            return ko(new Error(`unable to determine host from issuer url ${issuerUrl}`));
        }
        const socket = tls.connect(port, purl.host, { rejectUnauthorized: false });
        socket.once('error', ko);
        socket.once('secureConnect', () => {
            const cert = socket.getPeerCertificate();
            socket.end();
            const thumbprint = cert.fingerprint.split(':').join('');
            exports.external.log(`certificate authority thumbprint for ${issuerUrl} is ${thumbprint}`);
            ok(thumbprint);
        });
    });
}
// allows unit test to replace with mocks
/* eslint-disable max-len */
exports.external = {
    downloadThumbprint,
    log: defaultLogger,
    createOpenIDConnectProvider: (req) => iam().createOpenIDConnectProvider(req).promise(),
    deleteOpenIDConnectProvider: (req) => iam().deleteOpenIDConnectProvider(req).promise(),
    updateOpenIDConnectProviderThumbprint: (req) => iam().updateOpenIDConnectProviderThumbprint(req).promise(),
    addClientIDToOpenIDConnectProvider: (req) => iam().addClientIDToOpenIDConnectProvider(req).promise(),
    removeClientIDFromOpenIDConnectProvider: (req) => iam().removeClientIDFromOpenIDConnectProvider(req).promise(),
};
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZXh0ZXJuYWwuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyJleHRlcm5hbC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiO0FBQUEsMEJBQTBCOzs7QUFFMUIsMkJBQTJCO0FBQzNCLDJCQUEyQjtBQUMzQiw2REFBNkQ7QUFDN0QsK0JBQStCO0FBRS9CLElBQUksTUFBZSxDQUFDO0FBRXBCLFNBQVMsR0FBRztJQUNWLElBQUksQ0FBQyxNQUFNLEVBQUU7UUFBRSxNQUFNLEdBQUcsSUFBSSxHQUFHLENBQUMsR0FBRyxFQUFFLENBQUM7S0FBRTtJQUN4QyxPQUFPLE1BQU0sQ0FBQztBQUNoQixDQUFDO0FBRUQsU0FBUyxhQUFhLENBQUMsR0FBVyxFQUFFLEdBQUcsSUFBVztJQUNoRCxzQ0FBc0M7SUFDdEMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxHQUFHLEVBQUUsR0FBRyxJQUFJLENBQUMsQ0FBQztBQUM1QixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxLQUFLLFVBQVUsa0JBQWtCLENBQUMsU0FBaUI7SUFDakQsZ0JBQVEsQ0FBQyxHQUFHLENBQUMsb0RBQW9ELFNBQVMsRUFBRSxDQUFDLENBQUM7SUFDOUUsT0FBTyxJQUFJLE9BQU8sQ0FBUyxDQUFDLEVBQUUsRUFBRSxFQUFFLEVBQUUsRUFBRTtRQUNwQyxNQUFNLElBQUksR0FBRyxHQUFHLENBQUMsS0FBSyxDQUFDLFNBQVMsQ0FBQyxDQUFDO1FBQ2xDLE1BQU0sSUFBSSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsSUFBSSxFQUFFLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFHLENBQUM7UUFDdkQsSUFBSSxDQUFDLElBQUksQ0FBQyxJQUFJLEVBQUU7WUFDZCxPQUFPLEVBQUUsQ0FBQyxJQUFJLEtBQUssQ0FBQyw0Q0FBNEMsU0FBUyxFQUFFLENBQUMsQ0FBQyxDQUFDO1NBQy9FO1FBQ0QsTUFBTSxNQUFNLEdBQUcsR0FBRyxDQUFDLE9BQU8sQ0FBQyxJQUFJLEVBQUUsSUFBSSxDQUFDLElBQUksRUFBRSxFQUFFLGtCQUFrQixFQUFFLEtBQUssRUFBRSxDQUFDLENBQUM7UUFDM0UsTUFBTSxDQUFDLElBQUksQ0FBQyxPQUFPLEVBQUUsRUFBRSxDQUFDLENBQUM7UUFDekIsTUFBTSxDQUFDLElBQUksQ0FBQyxlQUFlLEVBQUUsR0FBRyxFQUFFO1lBQ2hDLE1BQU0sSUFBSSxHQUFHLE1BQU0sQ0FBQyxrQkFBa0IsRUFBRSxDQUFDO1lBQ3pDLE1BQU0sQ0FBQyxHQUFHLEVBQUUsQ0FBQztZQUNiLE1BQU0sVUFBVSxHQUFHLElBQUksQ0FBQyxXQUFXLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLElBQUksQ0FBQyxFQUFFLENBQUMsQ0FBQztZQUN4RCxnQkFBUSxDQUFDLEdBQUcsQ0FBQyx3Q0FBd0MsU0FBUyxPQUFPLFVBQVUsRUFBRSxDQUFDLENBQUM7WUFDbkYsRUFBRSxDQUFDLFVBQVUsQ0FBQyxDQUFDO1FBQ2pCLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQseUNBQXlDO0FBQ3pDLDRCQUE0QjtBQUNmLFFBQUEsUUFBUSxHQUFHO0lBQ3RCLGtCQUFrQjtJQUNsQixHQUFHLEVBQUUsYUFBYTtJQUNsQiwyQkFBMkIsRUFBRSxDQUFDLEdBQStDLEVBQUUsRUFBRSxDQUFDLEdBQUcsRUFBRSxDQUFDLDJCQUEyQixDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtJQUNsSSwyQkFBMkIsRUFBRSxDQUFDLEdBQStDLEVBQUUsRUFBRSxDQUFDLEdBQUcsRUFBRSxDQUFDLDJCQUEyQixDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtJQUNsSSxxQ0FBcUMsRUFBRSxDQUFDLEdBQXlELEVBQUUsRUFBRSxDQUFDLEdBQUcsRUFBRSxDQUFDLHFDQUFxQyxDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtJQUNoSyxrQ0FBa0MsRUFBRSxDQUFDLEdBQXNELEVBQUUsRUFBRSxDQUFDLEdBQUcsRUFBRSxDQUFDLGtDQUFrQyxDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtJQUN2Six1Q0FBdUMsRUFBRSxDQUFDLEdBQTJELEVBQUUsRUFBRSxDQUFDLEdBQUcsRUFBRSxDQUFDLHVDQUF1QyxDQUFDLEdBQUcsQ0FBQyxDQUFDLE9BQU8sRUFBRTtDQUN2SyxDQUFDIiwic291cmNlc0NvbnRlbnQiOlsiLyogaXN0YW5idWwgaWdub3JlIGZpbGUgKi9cblxuaW1wb3J0ICogYXMgdGxzIGZyb20gJ3Rscyc7XG5pbXBvcnQgKiBhcyB1cmwgZnJvbSAndXJsJztcbi8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBpbXBvcnQvbm8tZXh0cmFuZW91cy1kZXBlbmRlbmNpZXNcbmltcG9ydCAqIGFzIGF3cyBmcm9tICdhd3Mtc2RrJztcblxubGV0IGNsaWVudDogYXdzLklBTTtcblxuZnVuY3Rpb24gaWFtKCkge1xuICBpZiAoIWNsaWVudCkgeyBjbGllbnQgPSBuZXcgYXdzLklBTSgpOyB9XG4gIHJldHVybiBjbGllbnQ7XG59XG5cbmZ1bmN0aW9uIGRlZmF1bHRMb2dnZXIoZm10OiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKSB7XG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBuby1jb25zb2xlXG4gIGNvbnNvbGUubG9nKGZtdCwgLi4uYXJncyk7XG59XG5cbi8qKlxuICogRG93bmxvYWRzIHRoZSBDQSB0aHVtYnByaW50IGZyb20gdGhlIGlzc3VlciBVUkxcbiAqL1xuYXN5bmMgZnVuY3Rpb24gZG93bmxvYWRUaHVtYnByaW50KGlzc3VlclVybDogc3RyaW5nKSB7XG4gIGV4dGVybmFsLmxvZyhgZG93bmxvYWRpbmcgY2VydGlmaWNhdGUgYXV0aG9yaXR5IHRodW1icHJpbnQgZm9yICR7aXNzdWVyVXJsfWApO1xuICByZXR1cm4gbmV3IFByb21pc2U8c3RyaW5nPigob2ssIGtvKSA9PiB7XG4gICAgY29uc3QgcHVybCA9IHVybC5wYXJzZShpc3N1ZXJVcmwpO1xuICAgIGNvbnN0IHBvcnQgPSBwdXJsLnBvcnQgPyBwYXJzZUludChwdXJsLnBvcnQsIDEwKSA6IDQ0MztcbiAgICBpZiAoIXB1cmwuaG9zdCkge1xuICAgICAgcmV0dXJuIGtvKG5ldyBFcnJvcihgdW5hYmxlIHRvIGRldGVybWluZSBob3N0IGZyb20gaXNzdWVyIHVybCAke2lzc3VlclVybH1gKSk7XG4gICAgfVxuICAgIGNvbnN0IHNvY2tldCA9IHRscy5jb25uZWN0KHBvcnQsIHB1cmwuaG9zdCwgeyByZWplY3RVbmF1dGhvcml6ZWQ6IGZhbHNlIH0pO1xuICAgIHNvY2tldC5vbmNlKCdlcnJvcicsIGtvKTtcbiAgICBzb2NrZXQub25jZSgnc2VjdXJlQ29ubmVjdCcsICgpID0+IHtcbiAgICAgIGNvbnN0IGNlcnQgPSBzb2NrZXQuZ2V0UGVlckNlcnRpZmljYXRlKCk7XG4gICAgICBzb2NrZXQuZW5kKCk7XG4gICAgICBjb25zdCB0aHVtYnByaW50ID0gY2VydC5maW5nZXJwcmludC5zcGxpdCgnOicpLmpvaW4oJycpO1xuICAgICAgZXh0ZXJuYWwubG9nKGBjZXJ0aWZpY2F0ZSBhdXRob3JpdHkgdGh1bWJwcmludCBmb3IgJHtpc3N1ZXJVcmx9IGlzICR7dGh1bWJwcmludH1gKTtcbiAgICAgIG9rKHRodW1icHJpbnQpO1xuICAgIH0pO1xuICB9KTtcbn1cblxuLy8gYWxsb3dzIHVuaXQgdGVzdCB0byByZXBsYWNlIHdpdGggbW9ja3Ncbi8qIGVzbGludC1kaXNhYmxlIG1heC1sZW4gKi9cbmV4cG9ydCBjb25zdCBleHRlcm5hbCA9IHtcbiAgZG93bmxvYWRUaHVtYnByaW50LFxuICBsb2c6IGRlZmF1bHRMb2dnZXIsXG4gIGNyZWF0ZU9wZW5JRENvbm5lY3RQcm92aWRlcjogKHJlcTogYXdzLklBTS5DcmVhdGVPcGVuSURDb25uZWN0UHJvdmlkZXJSZXF1ZXN0KSA9PiBpYW0oKS5jcmVhdGVPcGVuSURDb25uZWN0UHJvdmlkZXIocmVxKS5wcm9taXNlKCksXG4gIGRlbGV0ZU9wZW5JRENvbm5lY3RQcm92aWRlcjogKHJlcTogYXdzLklBTS5EZWxldGVPcGVuSURDb25uZWN0UHJvdmlkZXJSZXF1ZXN0KSA9PiBpYW0oKS5kZWxldGVPcGVuSURDb25uZWN0UHJvdmlkZXIocmVxKS5wcm9taXNlKCksXG4gIHVwZGF0ZU9wZW5JRENvbm5lY3RQcm92aWRlclRodW1icHJpbnQ6IChyZXE6IGF3cy5JQU0uVXBkYXRlT3BlbklEQ29ubmVjdFByb3ZpZGVyVGh1bWJwcmludFJlcXVlc3QpID0+IGlhbSgpLnVwZGF0ZU9wZW5JRENvbm5lY3RQcm92aWRlclRodW1icHJpbnQocmVxKS5wcm9taXNlKCksXG4gIGFkZENsaWVudElEVG9PcGVuSURDb25uZWN0UHJvdmlkZXI6IChyZXE6IGF3cy5JQU0uQWRkQ2xpZW50SURUb09wZW5JRENvbm5lY3RQcm92aWRlclJlcXVlc3QpID0+IGlhbSgpLmFkZENsaWVudElEVG9PcGVuSURDb25uZWN0UHJvdmlkZXIocmVxKS5wcm9taXNlKCksXG4gIHJlbW92ZUNsaWVudElERnJvbU9wZW5JRENvbm5lY3RQcm92aWRlcjogKHJlcTogYXdzLklBTS5SZW1vdmVDbGllbnRJREZyb21PcGVuSURDb25uZWN0UHJvdmlkZXJSZXF1ZXN0KSA9PiBpYW0oKS5yZW1vdmVDbGllbnRJREZyb21PcGVuSURDb25uZWN0UHJvdmlkZXIocmVxKS5wcm9taXNlKCksXG59O1xuIl19