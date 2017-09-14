import cv2
import numpy as np
from board import Board
try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


def show(image):
    cv2.imshow('', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def remove_rows(img):
    """
    Removes horizontal lines from image
    """
    img2 = img.copy()
    rows_to_del = []
    for i, row in enumerate(img2):
        if max(row) == min(row):
            rows_to_del.append(i)
    for i in reversed(rows_to_del):
        img2 = np.delete(img2, i, 0)
    return img2


def remove_cols(img):
    """
    Removes vertical lines from image
    """
    return np.transpose(remove_rows(np.transpose(img)))


def read_digit(img):
    """
    Converts image of a number to float
    """
    pil = Image.fromarray(img.astype('uint8'))
    num = pytesseract.image_to_string(pil, config='--psm 10 -c tessedit_char_whitelist=123456789')
    return float(num)


def read_file(filename):
    return cv2.imread(filename)


def resize(img, max_height=1000.):
    if len(img) > max_height:
        new_height = max_height
        new_width = len(img[0]) / (len(img) / max_height)
        return cv2.resize(img, (int(new_height), int(new_width)))


def preprocess(img):
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # apply gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # apply threshold/morph
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # remove row and column lines
    img = remove_cols(img)
    return remove_rows(img)


def define_digit_boxes(img, display=False):
    cnts = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    boxes = []
    for c in cnts:
        box = cv2.boundingRect(c)
        if 500 > box[2] > 5 and 500 > box[3] > 5:
            boxes.append(box)

    if display:
        img2 = img.copy()
        for (x, y, w, h) in boxes:
            cx = x / (len(img) / 9)
            cy = y / (len(img[0]) / 9)
            string = '({}, {})'.format(cx, cy)
            cv2.rectangle(img2, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(img2, string, (x+w-60, y+h+20), color=(255, 0, 0), fontFace=1, fontScale=1)
        show(img2)

    return boxes


def populate_board(img, boxes):
    """
    Populates board with OCR'd numbers from img
    """
    board = np.zeros((9, 9))
    for (x, y, w, h) in boxes:
        cx = x / (len(img) / 9)
        cy = y / (len(img[0]) / 9)
        board[cx][cy] = read_digit(img[y - 10:y + h + 10, x - 10:x + w + 10])

    board = np.transpose(board).tolist()
    return [[int(x) for x in row] for row in board]


def solve_board(board):
    solvable = Board(board=board)  # worst line of code ever
    solvable.solve()  # second worst line of code ever
    return solvable.answer


def paint_answers(img, answers):
    img = img.copy()
    factor = len(img) / 9
    for x, row in enumerate(answers):
        for y, val in enumerate(row):
            if val > 0:
                cv2.putText(img, str(val), (int((y + 0.25) * factor), int((x + 0.75) * factor)),
                            color=(0, 0, 255), fontFace=1, fontScale=4)

    return img


if __name__ == '__main__':

    img = read_file('game_img_1.png')
    img = resize(img, 1000.)
    original = img.copy()
    show(original)
    preprocessed = preprocess(img)
    boxes = define_digit_boxes(preprocessed)

    board = populate_board(preprocessed, boxes)
    answers = solve_board(board)
    result_img = paint_answers(original, answers)
    show(result_img)
