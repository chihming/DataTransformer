import multiprocessing
from sys import stderr

def parallel_get_similarity(nn, tlist, nlist, alpha_len, topk, threshold=0.2, method='cosine'):
    scores = {}
    sim = {}
    for e, a in enumerate(tlist):
        scores.clear()
        s1 = nn[a]
        l1 = alpha_len[0][a]
        for b in nlist:
            if a == b:
                scores[b] = 1.
                continue
            score = len( s1 & nn[b] ) / ( (l1)*(alpha_len[1][b]) )
            if score > threshold:
                scores[b] = score

        pairs = []
        for k, v in sorted(scores.iteritems(), key=lambda (k, v): (v, k), reverse=True)[:topk]:
            pairs.append("%s:%f" % (k, v))
        sim[a] = "|".join(pairs)

        if e % 100 == 0: stderr.write('.')

    return sim


class FeatureMaker:

    def __init__(self, logger):
        self.logger = logger
        pass       

    def pairwise_similarity(self, nn, topk, alpha, threshold=0.1, method='cosine', process=1):
        nn = { key:set(nn[key]) for key in nn } # get unique elements
        in_alpha = 1 - alpha
        alpha_len = {}
        alpha_len[0] = { key:len(nn[key])**alpha for key in nn }
        alpha_len[1] = { key:len(nn[key])**in_alpha for key in nn }
        nlist = nn.keys()
        
        start = 0
        step = len(nlist)/process
        results = []
        sim = {}
        pool = multiprocessing.Pool(processes=process)

        for i in range(process):
            self.logger.info("Process %d start" % (i))
            tlist = nlist[start:start+step]
            results.append( pool.apply_async( parallel_get_similarity, args=(nn, tlist, nlist, alpha_len, topk ) ))
            start += step
        pool.close()
        pool.join()

        for res in results:
            sim.update( res.get() )
        
        stderr.write('\n')

        return sim
