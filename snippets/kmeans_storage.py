@task(returns = 1, labels = INOUT)
def cluster_and_partial_sums(fragment, labels, centres, norm):
  '''Given a fragment of points, declare a CxD matrix A and, for each point p:
  1) Compute the nearest centre c of p
  2) Add p / num_points_in_fragment to A[index(c)]
  3) Set label[index(p)] = c
  '''
  ret = np.matrix(np.zeros(centres.shape))
  n = fragment.mat.shape[0]
  c = centres.shape[0]
  # Check if labels is an empty list
  if not labels:
    # If it is, fill it with n zeros.
    for _ in range(n):
      # Done this way to not lose the reference
      labels.append(0)
  # Compute the big stuff
  associates = np.zeros(c)
  # Get the labels for each point
  for (i, point) in enumerate(fragment.mat):
    distances = np.zeros(c)
    for (j, centre) in enumerate(centres):
      distances[j] = np.linalg.norm(point - centre, norm)
    labels[i] = np.argmin(distances)
    associates[labels[i]] += 1
  # Add each point to its associate centre
  for (i, point) in enumerate(fragment.mat):
    ret[labels[i]] += point / associates[labels[i]]
  return ret


def kmeans_frag(fragments, dimensions, num_centres = ...):
  '''A fragment-based K-Means algorithm.
  Given a set of fragments (which can be either PSCOs or future objects that
  point to PSCOs), the desired number of clusters and the maximum number of
  iterations, compute the optimal centres and the index of the centre
  for each point.
  PSCO.mat must be a NxD float np.matrix, where D = dimensions
  '''
  import numpy as np
  # Choose the norm among the available ones
  norms = {
    'l1': 1,
    'l2': 'fro'
  }
  # Set the random seed
  np.random.seed(seed)
  # Centres is usually a very small matrix, so it is affordable to have it in
  # the master.
  centres = np.matrix(
    [np.random.random(dimensions) for _ in range(num_centres)]
  )
  # Make a list of labels, treat it as INOUT
  # Leave it empty at the beggining, update it inside the task. Avoid
  # having a linear amount of stuff in master's memory unnecessarily
  labels = [[] for _ in range(len(fragments))]
  # Note: this implementation treats the centres as files, never as PSCOs.
  for it in range(iterations):
    partial_results = []
    for (i, frag) in enumerate(fragments):
      # For each fragment compute, for each point, the nearest centre.
      # Return the mean sum of the coordinates assigned to each centre.
      # Note that mean = mean ( sum of sub-means )
      partial_result = cluster_and_partial_sums(frag, labels[i], centres, norms[norm])
      partial_results.append(partial_result)
    # Bring the partial sums to the master, compute new centres when syncing
    new_centres = np.matrix(np.zeros(centres.shape))
    from pycompss.api.api import compss_wait_on
    for partial in partial_results:
      partial = compss_wait_on(partial)
      # Mean of means, single step
      new_centres += partial / float( len(fragments) )
    if np.linalg.norm(centres - new_centres, norms[norm]) < epsilon:
      # Convergence criterion is met
      break
    # Convergence criterion is not met, update centres
    centres = new_centres
  # If we are here either we have converged or we have run out of iterations
  # In any case, now it is time to update the labels in the master
  ret_labels = []
  for label_list in labels:
    from pycompss.api.api import compss_wait_on
    to_add = compss_wait_on(label_list)
    ret_labels += to_add
  return centres, ret_labels
