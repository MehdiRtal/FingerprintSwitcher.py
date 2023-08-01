const {plugin} = require("browser-with-fingerprints");
const {readFile} = require("fs/promises");
const {ArgumentParser} = require("argparse");

const parser = new ArgumentParser();
parser.add_argument("--headless", {action: "store_true", default: false});
parser.add_argument("--proxy");
parser.add_argument("--user-data-dir", {dest: "userDataDir"});
let args = parser.parse_args();

async function main() {
    try {
        plugin.useFingerprint(
            await readFile(
                `fingerprints/${Math.floor(Math.random() * 10199) + 0}.json`,
                "utf8"
            ),
            {
                changeGeolocation: true,
                safeElementSize: true,
            }
        );
        if (args.proxy) {
            plugin.useProxy(`http://${args.proxy}/`, {
                changeGeolocation: true,
            });
        }
        browser = await plugin.spawn({
            headless: args.headless,
            userDataDir: args.userDataDir,
            args: ["--incognito"],
        });
        console.log(
            JSON.stringify({
                status: "success",
                url: `${browser.url}:${browser.port}`,
            })
        );
    } catch (e) {
        console.log(JSON.stringify({status: "error", message: e.message}));
    }
}
main();
