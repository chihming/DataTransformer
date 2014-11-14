from sys import stderr

class FeatureMaker:

    def __init__(self):
        pass

    def pairwise_similarity(self, dic, topk=10, alpha=0.5, threshold=0.1, method='cosine'):
        S = { k:set(dic[k]) for k in dic} # Sets
        L = { k:len(S[k]) for k in S } # Lenghts
        in_alpha = 1 - alpha
        sim = {}
        scores = {}
        for e, a in enumerate(S.keys()):
            scores.clear()
            s1 = S[a]
            l1 = L[a]**alpha
            for b in S.keys():
                if a == b:
                    scores[b] = 0.5
                    continue
                score = len( s1 & S[b] ) / ( (l1)*(L[b]**in_alpha) )
                if score > threshold:
                    scores[b] = score

            pairs = []
            for k, v in sorted(scores.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:topk]:
                pairs.append("%s:%f" % (k, v))
            sim[a] = "|".join(pairs)

            if e % 100 == 0: stderr.write('.')

        stderr.write('\n')
        return sim
