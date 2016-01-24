#!/usr/bin/env python

# Copyright (c) 2016 Matthew Earl
# # Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
# 
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
#     NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#     DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#     OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
#     USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import glob
import json
import logging
import os

import pada.align
import pada.framedrop
import pada.landmarks


APP_NAME = "pada"
APP_AUTHOR = "matthewearl"
CONFIG_FILE_NAME = "pada.conf"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='Print debug information',
                        action='store_true')
    parser.add_argument('--config', help='Config file path', type=unicode,
                        default=CONFIG_FILE_NAME)

    subparsers = parser.add_subparsers(help='Sub-command help')

    align_parser = subparsers.add_parser('align',
                                         help='align a set of images')
    align_parser.add_argument('--input-glob',
                              help='Input files glob', type=unicode)
    align_parser.add_argument('--out-path',
                              help='Path to write files to', type=unicode)
    align_parser.add_argument('--predictor-path',
                              help='DLib face predictor dat file',
                              type=unicode)
    align_parser.add_argument('--img-thresh',
                              help='Max duplicate frame delta', type=float)
    align_parser.set_defaults(cmd='align')

    framedrop_parser = subparsers.add_parser(
                                       'framedrop',
                                       help='Drop frames from a set of images')
    framedrop_parser.add_argument('--input-glob', help='Input files glob',
                                  type=unicode)
    framedrop_parser.add_argument('--out-file',
                              help='Path to write file list to', type=unicode)
    framedrop_parser.add_argument('--predictor-path',
                                  help='DLib face predictor dat file',
                                  type=unicode)
    framedrop_parser.add_argument('--erode-amount',
                              help='Amount to erode face mask by', type=int)
    framedrop_parser.set_defaults(cmd='framedrop')

    return parser.parse_args()


if __name__ == "__main__":
    cli_args = parse_args()
    if cli_args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Build up a list of potential config files to parse.
    config_paths = []
    try:
        import appdirs
    except ImportError:
        logging.warn("appdirs not installed, not reading site/user config")
    else:
        config_paths.append(
            os.path.join(
                appdirs.user_config_dir(APP_NAME, APP_AUTHOR),
                CONFIG_FILE_NAME))
        config_paths.append(
            os.path.join(
                appdirs.site_config_dir(APP_NAME, APP_AUTHOR),
                CONFIG_FILE_NAME))
    if cli_args.config:
        config_paths.append(cli_args.config)

    # Attempt to open each config file, and update the `cfg` dict with each
    # one.
    cfg = {}
    for config_path in config_paths:
        try:
            with open(config_path) as f:
                d = json.load(f)
                cfg.update(d[cli_args.cmd])
        except IOError:
            logging.warn("Could not open config file %s", config_path)
        else:
            logging.info("Read config file %s", config_path)

    # Add CLI arguments to the `cfg` dict.
    cfg.update((k, v) for k, v in cli_args.__dict__.items() if v is not None)
    logging.debug("Config is %r", cfg)

    # Execute the command by deferring to the appopriate module.
    if cli_args.cmd == "align":
        landmark_finder = pada.landmarks.LandmarkFinder(cfg['predictor_path'])
        pada.align.align_images(
            input_files=glob.glob(cfg['input_glob']),
            out_path=cfg['out_path'],
            landmark_finder=landmark_finder,
            img_thresh=cfg['img_thresh'])
    elif cli_args.cmd == "framedrop":
        landmark_finder = pada.landmarks.LandmarkFinder(cfg['predictor_path'])
        pada.framedrop.filter_files(
            input_files=glob.glob(cfg['input_glob']),
            frame_skip=cfg['frame_skip'],
            erode_amount=cfg['erode_amount'],
            landmark_finder=landmark_finder)
