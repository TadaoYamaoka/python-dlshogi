import shogi
import shogi.CSA
import copy

import argparse
import logging
import os
import numpy as np
import re
from tqdm import tqdm

from pydlshogi.features import *

logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', 
    datefmt='%Y/%m/%d %H:%M:%S', 
    level=os.environ.get("LOGLEVEL", "DEBUG"))


# 保存済みのダンプファイルを読み込む
def load_dump(filename):
    logging.info('Loading from %s' % (filename))
    with open(filename, 'rb') as f:
        positions = np.load(f)
    return positions


# ファイルに棋譜データをダンプする
def save_dump(filename, positions):
    logging.info('Saving to %s' % (filename))
    np.array(positions).dump(filename)


# read kifu
def read_kifu(kifu_list_file):
    logging.info('read kifu start')
    dump_fname = re.sub(r'\.[^\.]+$', '', kifu_list_file) + '.pickle'
    logging.info('dump_fname %s' % (dump_fname))
    if os.path.exists(dump_fname): return load_dump(dump_fname)

    positions = []
    with open(kifu_list_file, 'r') as f:
        for line in tqdm(f.readlines(), ncols=70):
            filepath = line.rstrip('\r\n')
            kifu = shogi.CSA.Parser.parse_file(filepath)[0]
            win_color = shogi.BLACK if kifu['win'] == 'b' else shogi.WHITE
            board = shogi.Board()
            for move in kifu['moves']:
                if board.turn == shogi.BLACK:
                    piece_bb = copy.deepcopy(board.piece_bb)
                    occupied = copy.deepcopy((board.occupied[shogi.BLACK], board.occupied[shogi.WHITE]))
                    pieces_in_hand = copy.deepcopy((board.pieces_in_hand[shogi.BLACK], board.pieces_in_hand[shogi.WHITE]))
                else:
                    piece_bb = [bb_rotate_180(bb) for bb in board.piece_bb]
                    occupied = (bb_rotate_180(board.occupied[shogi.WHITE]), bb_rotate_180(board.occupied[shogi.BLACK]))
                    pieces_in_hand = copy.deepcopy((board.pieces_in_hand[shogi.WHITE], board.pieces_in_hand[shogi.BLACK]))

                # move label
                move_label = make_output_label(shogi.Move.from_usi(move), board.turn)

                # result
                win = 1 if win_color == board.turn else 0

                positions.append((piece_bb, occupied, pieces_in_hand, move_label, win))
                board.push_usi(move)

    save_dump(dump_fname, positions)

    logging.info('read kifu end')
    return positions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kifulist', type=str, help='kifu list')
    args = parser.parse_args()
    read_kifu(args.kifulist)