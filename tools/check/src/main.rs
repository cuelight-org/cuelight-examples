//! Check every show listed in `examples.json`.
//!
//! ```sh
//! cargo run --manifest-path tools/check/Cargo.toml
//! ```
//!
//! Every show is loaded like the player does, with its sounds decoded,
//! and audited with `cuelight_loader::audit` over its document, its
//! folder and its driver script. A show fails the run when it does not
//! load, when an asset has no decoder or a sound does not decode, or when
//! the audit finds an `error` (what a strict load refuses) or a `missing`
//! (a file, name or trigger nothing provides). Findings of the `unused`
//! and `unwise` kinds are printed as notes and fail nothing: a feature
//! example may well keep a layer hidden on purpose. Needs no GPU.

use cuelight::Engine;
use cuelight_audio::Sound;
use cuelight_core::FindingKind;
use cuelight_loader::Manifest;
use std::path::Path;

fn main() -> std::process::ExitCode {
    match run() {
        Ok(()) => std::process::ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("{e}");
            std::process::ExitCode::FAILURE
        }
    }
}

fn run() -> Result<(), Box<dyn std::error::Error>> {
    let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    let catalog: serde_json::Value =
        serde_json::from_str(&std::fs::read_to_string(root.join("examples.json"))?)?;
    let mut problems = 0;
    let mut notes = 0;
    let examples = catalog["categories"]
        .as_array()
        .into_iter()
        .flatten()
        .flat_map(|category| category["examples"].as_array().into_iter().flatten());
    for example in examples {
        let path = example["path"]
            .as_str()
            .ok_or("an example without a path")?;
        let dir = root.join(path);

        let mut engine = Engine::new();
        let mut loaded = match cuelight_loader::load(&mut engine, &dir) {
            Ok(loaded) => loaded,
            Err(e) => {
                eprintln!("{path}: {e}");
                problems += 1;
                continue;
            }
        };
        for skipped in &loaded.skipped {
            eprintln!("{path}: asset {skipped:?} has no decoder");
            problems += 1;
        }
        for file in &loaded.sounds {
            if let Err(e) = Sound::decode(&file.extension, &file.bytes) {
                eprintln!("{path}: sound {:?}: {e}", file.name);
                problems += 1;
            }
        }
        // The loader parsed the driver script that came with the show;
        // the audit takes it with the document and the folder's files.
        let driver = loaded.driver.take();
        let json = std::fs::read_to_string(dir.join("show.json"))?;
        let manifest = Manifest::for_dir(&dir)?;
        for finding in cuelight_loader::audit(&json, Some(&manifest.files), driver.as_ref()) {
            let kind = finding.kind.name();
            eprintln!("{path}: {kind}: {}: {}", finding.path, finding.message);
            match finding.kind {
                FindingKind::Error | FindingKind::Missing => problems += 1,
                _ => notes += 1,
            }
        }
        println!("{path}: ok");
    }
    if notes > 0 {
        eprintln!("{notes} note(s): unused or unwise, for the reader to weigh");
    }
    if problems > 0 {
        return Err(format!("{problems} problem(s)").into());
    }
    Ok(())
}
