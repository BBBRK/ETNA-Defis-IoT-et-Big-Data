<?php

require __DIR__ . '/vendor/autoload.php';
require '/usr/local/lib/cloudi-2.0.0/api/php/CloudI.php';

use \InfluxDB\Client;

class Task
{
    private $api;

    public function __construct($api)
    {
        $this->api = $api;
    }

    public function run()
    {
        try
        {
            $this->api->subscribe('query/get',
            $this, 'query');
            $this->api->poll();
        }
        catch (CloudI\TerminateException $e)
        {
        }
        catch (Exception $e)
        {
            error_log("{$e->getMessage()}\n{$e}\n");
        }
    }

    public function query($request_type, $name, $pattern,
                                $request_info, $request,
                                $timeout, $priority,
                                $trans_id, $pid)
    {
        $host = "127.0.0.1";
        $port = "8086";

        $client = new Client($host, $port);
        $database = $client->selectDB('mmp');
        $result = $database->query("SELECT * FROM mmp_metrics where time > '2018-08-27 06:56:10' AND time < '2018-08-27 06:58:10'");
        $points = $result->getPoints();
        return $points;
    }
}

$thread_count = CloudIAPI::thread_count();
assert($thread_count == 1);
$main_thread = new Task(new CloudIAPI(0));
$main_thread->run();

?>

curl -X POST -d @query.conf \
    http://localhost:6464/cloudi/api/rpc/services_add.erl
