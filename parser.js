// Credit: https://github.com/PerseverantDT/osu-mania-parser

const { dir } = require('console');
const fs = require('fs');
var path = require('path');
const { emitWarning, exit } = require('process');
const { getSystemErrorMap } = require('util');

"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseFileSync = void 0;

function parseFileSync(path) {
    if (!fs.existsSync(path)) {
        return;
    }
    let beatmap = new Beatmap();
    let sectionReg = /^\[([a-zA-Z0-9]+)\]$/;
    let contents = fs.readFileSync(path, {
        encoding: 'utf8'
    }).split('\r\n').filter(value => !(value.startsWith('//') || value === ''));
    let sectionToRead = "";
    for (let line of contents) {
        let match = sectionReg.exec(line);
        if (match !== null) {
            sectionToRead = match[1];
        }
        else {
            switch (sectionToRead) {
                case "General":
                    let gen = line.split(": ");
                    gen.push('');
                    if (gen[0] === "Mode") {
                        switch (gen[1]) {
                            case '3':
                                break;
                            default:
                                return;
                        }
                    }
                    else if (gen[0] === "PreviewTime")
                        beatmap.previewTime = parseInt(gen[1]);
                    else if (gen[0] === "AudioFilename")
                        beatmap.audioFile = gen[1];
                    else if (gen[0] === "Countdown")
                        beatmap.countDown = gen[1];
                    break;
                case "Metadata":
                    let mdata = line.split(":");
                    if (mdata[0] === "Title")
                        beatmap.title = mdata[1];
                    else if (mdata[0] === "TitleUnicode")
                        beatmap.titleUnicode = mdata[1];
                    else if (mdata[0] === "Artist")
                        beatmap.artist = mdata[1];
                    else if (mdata[0] === "Creator")
                        beatmap.creator = mdata[1];
                    else if (mdata[0] === "Version")
                        beatmap.diffname = mdata[1];
                    else if (mdata[0] === "Tags")
                        beatmap.tags = mdata[1].split(' ');
                    else if (mdata[0] === "BeatmapID")
                        beatmap.mapId = parseInt(mdata[1]);
                    else if (mdata[0] === "BeatmapSetID")
                        beatmap.mapsetId = parseInt(mdata[1]);
                    break;
                case "Difficulty":
                    let diff = line.split(":");
                    diff.push('');
                    if (diff[0] === "HPDrainRate")
                        beatmap.hpDrain = parseFloat(diff[1]);
                    if (diff[0] === "CircleSize")
                        beatmap.keyCount = parseInt(diff[1]);
                    if (diff[0] === "OverallDifficulty")
                        beatmap.difficulty = parseFloat(diff[1]);
                    break;
                case "TimingPoints":
                    beatmap.addTimingPoint(line);
                    break;
                case "HitObjects":
                    beatmap.addHitObject(line);
                    break;
            }
        }
    }
    beatmap.keyPositions.sort((a, b) => a - b);
    return beatmap;
}
exports.parseFileSync = parseFileSync;

class Beatmap {
    constructor() {
        this.audioFile = "";
        this.countDown = "";
        this.title = "";
        this.titleUnicode = "";
        this.artist = "";
        this.creator = "";
        this.diffname = "";
        this.source = "";
        this.previewTime = 0;
        this.tags = [];
        this.mapId = 0;
        this.mapsetId = 0;
        this.keyCount = 0;
        this.hpDrain = 0;
        this.difficulty = 0;
        this.minBpm = 0;
        this.maxBpm = 0;
        this.nbNotes = 0;
        this.nbHolds = 0;
        this.timingPoints = [];
        this.hitObjects = [];
        this.keyPositions = [];
    }
    getTimingPoint(time) {
        for (var i = this.timingPoints.length - 1; i >= 0; i--) {
            if (this.timingPoints[i].time <= time) {
                return this.timingPoints[i];
            }
        }
        return this.timingPoints[0];
    }
    addTimingPoint(line) {
        var _a, _b, _c, _d, _e, _f;
        let timingPoint = TimingPoint.parse(line);
        if (this.minBpm === 0)
            this.minBpm = (_a = timingPoint.bpm) !== null && _a !== void 0 ? _a : 0;
        else if (this.minBpm > ((_b = timingPoint.bpm) !== null && _b !== void 0 ? _b : Infinity))
            this.minBpm = (_c = timingPoint.bpm) !== null && _c !== void 0 ? _c : 0;
        if (this.maxBpm === 0)
            this.maxBpm = (_d = timingPoint.bpm) !== null && _d !== void 0 ? _d : 0;
        else if (this.maxBpm < ((_e = timingPoint.bpm) !== null && _e !== void 0 ? _e : -Infinity))
            this.maxBpm = (_f = timingPoint.bpm) !== null && _f !== void 0 ? _f : 0;
        this.timingPoints.push(timingPoint);
    }
    addHitObject(line) {
        let hitObject = HitObject.parse(line);
        if (hitObject)
        {
            if (hitObject.type === 'note')
                this.nbNotes++;
            else if (hitObject.type === 'hold')
                this.nbHolds++;
            if (this.keyPositions.findIndex(item => item === hitObject.x) === -1) {
                this.keyPositions.push(hitObject.x);
            }
            this.hitObjects.push(hitObject);
        }
    }
}
class TimingPoint {
    constructor(time, bpm, velocity, meter, sampleSet, sampleIndex, volume, uninherited, kiaiTime, omitFirstBarLine) {
        this.time = time;
        if (bpm !== 0)
            this.bpm = bpm;
        this.timingSignature = meter;
        this.velocity = velocity;
        this.sampleSet = sampleSet;
        this.sampleIndex = sampleIndex;
        this.volume = volume;
        this.uninherited = uninherited;
        this.kiaiTime = kiaiTime;
        this.omitFirstBarLine = omitFirstBarLine;
    }
    static parse(line) {
        let members = line.split(',');
        let beatLength = parseFloat(members[1]);
        let bpm = 0;
        let velocity = 1;
        if (beatLength > 0)
            bpm = Math.round(60000 / beatLength);
        else
            velocity = Math.abs(100 / beatLength);
        let effects = parseInt(members[7]);
        return new TimingPoint(parseInt(members[0]), bpm, velocity, parseInt(members[2]), parseInt(members[3]), parseInt(members[4]), parseInt(members[5]), members[6] === '1', ((effects & 0b1) !== 0), ((effects & 0b100) !== 0));
    }
}
class HitObject {
    constructor(type, hitsound, newCombo, comboColorsSkipped, x, y, time, endTime) {
        this.type = type;
        this.hitSound = hitsound;
        this.newCombo = newCombo;
        this.comboColorsSkipped = comboColorsSkipped;
        this.x = x;
        this.y = y;
        this.time = time;
        this.endTime = endTime;
    }
    static parse(line) {
        let members = line.split(',');
        let type = parseInt(members[3]);
        let note = false;
        let hold = false;
        if ((type & 0b1) === 1)
            note = true;
        else if ((type & 0b10000000))
            hold = true;
        let newCombo = (type & 0b100) === 1;
        let comboColorsSkipped = (type & 0b11100) / 4;
        let hitsoundFlags = parseInt(members[4]);
        let hitsounds = [];
        if ((hitsoundFlags & 0b1) === 1)
            hitsounds.push('normal');
        if ((hitsoundFlags & 0b10) === 1)
            hitsounds.push('whistle');
        if ((hitsoundFlags & 0b100) === 1)
            hitsounds.push('finish');
        if ((hitsoundFlags & 0b1000) === 1)
            hitsounds.push('clap');
        if (hitsounds.length === 0)
            hitsounds.push('normal');
        if (note) {
            return new HitObject('note', hitsounds, newCombo, comboColorsSkipped, parseInt(members[0]), parseInt(members[1]), parseInt(members[2]), parseInt(members[2]));
        }
        else if (hold) {
            return new HitObject('hold', hitsounds, newCombo, comboColorsSkipped, parseInt(members[0]), parseInt(members[1]), parseInt(members[2]), parseInt(members[5].split(':')[0]));
        }
        else { return; }
    }
}

let s = 0;
let t = 0;
function parseALL(startPath, filter) {

    var files = fs.readdirSync(startPath);
    for (var i = 0; i < files.length; i++) {
        var filename = path.join(startPath, files[i]);
        var stat = fs.lstatSync(filename);
        if (stat.isDirectory()) {
            parseALL(filename, '.osu');
        } else if (filename.endsWith(filter)) {
            try {
                var beatmap = parseFileSync(filename);
                if (!fs.existsSync("./maps/" + beatmap.title + " - " + beatmap.diffname + "/")){
                    fs.mkdirSync("./maps/" + beatmap.title + " - " + beatmap.diffname + "/");
                    fs.copyFileSync(path.join(filename, "/../"+beatmap.audioFile), "./maps/" + beatmap.title + " - " + beatmap.diffname + "/audio.mp3");
                    fs.writeFileSync("./maps/" + beatmap.title + " - " + beatmap.diffname + "/beatmap.json", JSON.stringify(beatmap, null, 4))
                    s++;
                    t++;
                }
            }
            catch (_) {
                t++;
            }
        };
    };
};

const readline = require("readline");
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

if (!fs.existsSync("./maps/")){
    fs.mkdirSync("./maps/");
}

var userName = process.env['USERPROFILE'].split(path.sep)[2];
var songdir = 'C:\\Users\\' + userName + '\\AppData\\Local\\osu!\\Songs';

if (fs.existsSync(songdir) && fs.lstatSync(songdir).isDirectory()) {
    console.log("Parsing...");
    parseALL(songdir , '.osu');
    console.log("Successfully parsed " + s + " new beatmaps.");
    console.log((t-s).toString() + " beatmaps failed to parse.");
}
else
{
    console.log("Your osu songs directory was not automatically found. In order to parse, you must enter your osu songs directory.");
    rl.question("Song Directory: ", function(dirp) {
        if (fs.existsSync(dirp) && fs.lstatSync(dirp).isDirectory()) {
            rl.close();
            console.log("Parsing...");
            parseALL(dirp, '.osu');
            console.log("Successfully parsed " + s + " new beatmaps.");
            console.log((t-s).toString() + " beatmaps failed to parse.");
        }
        else
        {
            console.log("Invalid directory.");
            rl.close();
            exit();
        }
    });
}