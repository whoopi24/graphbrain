import logging

import graphbrain.patterns
from graphbrain import hedge
from graphbrain.semsim.matcher import SemSimMatcher, SemSimConfig

logger = logging.getLogger(__name__)

DEFAULT_CONFIG: SemSimConfig(
    model_name='word2vec-google-news-300',
    similarity_threshold=0.0
)

matcher: SemSimMatcher | None = None


def init_matcher(config: SemSimConfig | None = None):
    global matcher
    matcher = SemSimMatcher(config) if config else SemSimMatcher(DEFAULT_CONFIG)
    return matcher


def semsim(candidate: str, references: list[str], threshold: float = None) -> bool:
    global matcher
    if not matcher:
        init_matcher()
    return matcher.similar(candidate, references, threshold)


def match_semsim(pattern, edge, curvars=None, hg=None) -> list[dict]:
    if edge.not_atom:
        return []

    edge_word_part: str = edge.parts()[0]

    # possibly multi-word semsim
    pattern_word_part: str = pattern[0].parts()[0]

    if pattern_word_part.startswith('[') and pattern_word_part.endswith(']'):
        pattern_words = [w.strip() for w in pattern_word_part[1:-1].split(',')]
    else:
        pattern_words = [pattern_word_part]

    # extract similarity threshold if given
    similarity_threshold: float | None = _extract_similarity_threshold(pattern)

    logger.debug(f"edge: {str(edge)} | word part: {edge_word_part} | "
                 f"pattern: {str(pattern)} | threshold: {similarity_threshold}")

    if not semsim(edge_word_part, pattern_words, similarity_threshold):
        return []

    # replace first edge part with pattern word part
    edge_parts_modified = [edge_part if idx != 0 else pattern_word_part for idx, edge_part in enumerate(edge.parts())]
    edge_modified = hedge('/'.join(edge_parts_modified))

    if graphbrain.patterns._matches_atomic_pattern(edge_modified, pattern[0]):
        return [curvars]

    return []


def _extract_similarity_threshold(pattern: str) -> float | None:
    if not len(pattern) > 1:
        return None

    try:
        similarity_threshold = float(pattern[1][0])
    except ValueError:
        logger.error(f"Invalid value for similarity threshold: {pattern[1]}")
        return None

    return similarity_threshold
