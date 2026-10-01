# OLL/PLL Alg Log

A tracker for learning Rubik's cube last-layer algorithms — all 57 OLL and 21 PLL cases, plus your own custom algs (F2L, alternates, anything).

**Use it:** https://jadenzou1-dotcom.github.io/oll-pll-alg-log/

## Features

- Case diagrams for every OLL/PLL case, generated from real cube states (OLL shown in top-color-only style, PLL in full color)
- Per-case algorithm, notes, and nickname fields
- Mastery checkboxes: learned, 4-angle recognition, pre/post AUFs practiced, alt angle/alg
- Progress bars, a learned-per-month chart, and a dated activity log
- Filter by OLL shape / PLL category, learned vs. remaining, or search
- PLL comes pre-filled with common algs from SpeedCubeDB — edit freely
- Export / import a JSON backup

## Install as an app

It's a single-page web app, so there's nothing to download:

- **iPhone/iPad:** open the link in Safari → Share → *Add to Home Screen*
- **Android / desktop Chrome:** open the link → menu → *Install app*

## Your data

Everything is saved in your browser's `localStorage` — nothing is sent anywhere. That also means it's per-device and per-browser, so use **Export backup** to save a copy or move it to another device.

## Run locally

Just open `index.html` in a browser. No build step, no dependencies.
