import argparse
from gensim.models import Word2Vec
from pathlib import Path
import json
import multiprocessing
import os

cores = multiprocessing.cpu_count()


def train_word2vec(corpus_path, workers=cores - 1):
    # Parameters set based on Baroni et al. (2014)   DOI: 10.3115/v1/P14-1023
    model = Word2Vec(
        vector_size=400,
        window=5,
        negative=10,
        sample=1e-5,
        min_count=5,
        workers=workers,
        epochs=5
    )
    model.build_vocab(corpus_file=corpus_path)
    total_words = sum(model.wv.get_vecattr(word, "count") for word in model.wv.index_to_key)
    model.train(
        corpus_file=corpus_path,
        total_examples=model.corpus_count,
        total_words=total_words,
        epochs=model.epochs
    )
    return model, model.corpus_count, total_words


def save_metadata(num_comments, total_words, model, out_dir):
    metadata = {
        "num_comments": num_comments,
        "total_tokens": int(total_words),
        "vocab_size": len(model.wv),
        "vector_size": model.vector_size,
    }
    with open(os.path.join(out_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def main(args):
    model, num_comments, total_words = train_word2vec(args.input)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    model.save(str(out_dir / "word2vec.model"))  # secondo me posso evitare str() e usare f""
    model.wv.save_word2vec_format(str(out_dir / "vectors.txt"), binary=False)
    save_metadata(num_comments, total_words, model, str(out_dir))
    print(f"Model and vectors saved to {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to the .txt file with preprocessed comments")
    parser.add_argument("output_dir", help="Directory to save model, vectors, and metadata")
    args = parser.parse_args()
    main(args)
