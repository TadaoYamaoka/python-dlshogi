import shogi
import shogi.CSA
import copy

import argparse
import logging
import os
import _pickle as pickle
import re
from tqdm import tqdm

from pydlshogi.features import *

logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', 
    datefmt='%Y/%m/%d %H:%M:%S', 
    level=os.environ.get("LOGLEVEL", "DEBUG"))


# pickleファイルを読み込む
def load_pickle(pickle_filename):
    logging.info('Loading pickle %s' % (pickle_filename))
    with open(pickle_filename, 'rb') as f:
        positions = pickle.load(f)
    return positions


# pickleファイルを保存する
def save_pickle(pickle_filename, positions):
    logging.info('Saving pickle %s' % (pickle_filename))
    with open(pickle_filename, 'wb') as f:
        pickle.dump(positions, f, pickle.HIGHEST_PROTOCOL)
        logging.info('save pickle')


# read kifu
def read_kifu(kifu_list_file):
    logging.info('read kifu start')
    pickle_filename = re.sub(r'\.[^\.]+$', '', kifu_list_file) + '.pickle'
    logging.info('pickle_filename %s' % (pickle_filename))
    if os.path.exists(pickle_filename): return load_pickle(pickle_filename)

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

    save_pickle(pickle_filename, positions)

    logging.info('read kifu end')
    return positions


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kifulist', type=str, help='kifu list')
    args = parser.parse_args()
    read_kifu(args.kifulist)