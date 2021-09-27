# Assetto Corsa Virtual Wheel

![screenshot of plugin in action](screenie.jpg "lol")
<screenshot here>

This is a Python widget for Assetto Corsa that renders a basic wheel that illustrates the current sheering angle input.
Thanks to ckendell for the AC app tutorial that I found super helpful. https://github.com/ckendell/ACAppTutorial/blob/master/ACAppTutorial.md

## Installation
1. Extract the contents of `src` to `GAME_DIRECTORY/apps/python/virtualwheel`. This is typically `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\apps\python\virtualwheel`.
3. Enable this plugin in game settings. From game main menu: `Options` > `General` > `UI Modules`. Check `virtualwheel`.
4. Enter a session
5. Select `Virtual Wheel` from the widget list and drag the widget to your desired position.

## Release notes
v0.1: initial release

## Contributing
Always keen on PRs to improve this plugin with new features or bug fixes no matter how small.

1. Clone repo to disk
2. Make changes to source files in `src`
3. Make sure tests pass
4. Do an in-game test
5. Create PR
6. PR gets reviewed and probably merged by me. Thanks!

## Testing your changes (WIP)
TODO(EDWARD): set up regression testing and linter and add test status widgets.

Quick sanity check: run `test.py`. A pygame window will appear and display a wheel rotating. If it is not a wheel rotating, then something's not right!
```
cd src
pip install pygame
python test.py
```

