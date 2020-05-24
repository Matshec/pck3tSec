$worker_threads_count = $args[0]
$test_time_in_minutes = $args[1]

docker exec backend python testing/traffic_test.py  $worker_threads_count  $test_time_in_minutes